"""SQLAlchemy ORM models for TigerTaxi.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu),
Kwasi Oppong-Badu '22 (kyo@princeton.edu)
"""

# ----------------------------------------------------------------------

import enum
from datetime import datetime, timedelta

from sqlalchemy import func, or_

from tigertaxi.extensions import db

# ----------------------------------------------------------------------


def ride_departure_limit() -> datetime:
    """Returns a UTC datetime representing the ride departure limit.

    Rides which depart after this time should not be shown on any page
    in the application.
    """
    return datetime.utcnow() - timedelta(hours=6)


# ----------------------------------------------------------------------

BaseModel = db.Model


class AbstractModel(BaseModel):  # type: ignore
    """Base class for all TigerTaxi models.

    Defines columns and functions which are common to all models. Should
    be inherited before any other classes.
    """

    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    created_at = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
    )
    updated_at = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def save(cls) -> "AbstractModel":
        """Saves a model object in the database."""
        db.session.add(cls)
        db.session.commit()
        return cls

    def remove(cls) -> None:
        """Removes a model object from the database."""
        db.session.delete(cls)
        db.session.commit()


class User(AbstractModel):
    """Represents a TigerTaxi user."""

    __tablename__ = "users"

    # Fields
    netid = db.Column(
        db.String(64),
        index=True,
        unique=True,
        nullable=False,
    )
    email = db.Column(
        db.String(256),
        index=False,
        unique=True,
        nullable=False,
    )
    disp_name = db.Column(
        db.String(256),
        index=False,
        nullable=False,
    )
    phone_num = db.Column(
        db.String(16),
        index=False,
    )
    email_notifs = db.Column(
        db.Boolean,
        index=False,
        default=True,
    )
    text_notifs = db.Column(
        db.Boolean,
        index=False,
        default=True,
    )

    def query_outbound_requests(self):
        return (
            RideRequest.query.join(Ride, RideRequest.ride)
            .where(
                RideRequest.user_id == self.id,
                Ride.departure_datetime >= ride_departure_limit(),
            )
            .order_by(Ride.departure_datetime.asc())
        )

    def get_outbound_requests(self):
        return self.outbound_requests

    def get_pending_outbound_requests(self):
        return (
            self.query_outbound_requests()
            .where(
                RideRequest.status == RideRequest.Status.PENDING.value
            )
            .all()
        )

    def get_accepted_outbound_requests(self):
        return (
            self.query_outbound_requests()
            .where(
                RideRequest.status == RideRequest.Status.ACCEPTED.value
            )
            .all()
        )

    def get_rejected_outbound_requests(self):
        return (
            self.query_outbound_requests()
            .where(
                RideRequest.status == RideRequest.Status.REJECTED.value
            )
            .all()
        )

    def get_requests_outbox(self):
        return {
            "accepted": self.get_accepted_outbound_requests(),
            "pending": self.get_pending_outbound_requests(),
            "rejected": self.get_rejected_outbound_requests(),
        }

    def get_requests_inbox(self):
        return {
            "accepted": self.get_accepted_inbound_requests(),
            "pending": self.get_pending_inbound_requests(),
            "rejected": self.get_rejected_inbound_requests(),
        }

    def query_inbound_requests(self):
        return RideRequest.query.join(Ride, RideRequest.ride).where(
            Ride.creator_id == self.id
        )

    def get_inbound_requests(self):
        return self.query_inbound_requests().all()

    def get_pending_inbound_requests(self):
        return (
            self.query_inbound_requests()
            .where(
                RideRequest.status == RideRequest.Status.PENDING.value
            )
            .all()
        )

    def get_accepted_inbound_requests(self):
        return (
            self.query_inbound_requests()
            .where(
                RideRequest.status == RideRequest.Status.ACCEPTED.value
            )
            .all()
        )

    def get_rejected_inbound_requests(self):
        return (
            self.query_inbound_requests()
            .where(
                RideRequest.status == RideRequest.Status.REJECTED.value
            )
            .all()
        )

    def query_rides(self):
        created = Ride.query.where(Ride.creator_id == self.id)
        joined = Ride.query.join(Rider).where(Rider.user_id == self.id)

        return created.union(joined).order_by(
            Ride.departure_datetime.asc()
        )

    def get_created_rides(self):
        return (
            Ride.query.where(
                Ride.creator_id == self.id,
                Ride.departure_datetime >= ride_departure_limit(),
            )
            .order_by(Ride.departure_datetime.asc())
            .all()
        )

    def get_all_rides(self):
        return (
            self.query_rides()
            .order_by(Ride.departure_datetime.asc())
            .all()
        )

    def get_upcoming_rides(self):
        return (
            self.query_rides()
            .where(Ride.departure_datetime >= datetime.utcnow())
            .order_by(Ride.departure_datetime.asc())
            .all()
        )

    def __repr__(self):
        return "<User {}>".format(self.netid)


class Ride(AbstractModel):
    __tablename__ = "rides"

    # Ride fields
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    capacity = db.Column(
        db.Integer,
        index=False,
        nullable=False,
        default=2,
    )
    origin = db.Column(
        db.String(256),
        index=True,
        nullable=False,
        default="Princeton",
    )
    destination = db.Column(
        db.String(256),
        index=True,
        nullable=False,
        default="Princeton",
    )
    departure_datetime = db.Column(
        db.DateTime,
        index=True,
        nullable=False,
    )
    notes = db.Column(
        db.String(280),
        index=False,
        nullable=True,
    )
    is_anonymous = db.Column(
        db.Boolean,
        index=False,
        nullable=False,
        default=True,
    )

    # Relationships to other tables
    creator = db.relationship(
        "User",
        backref="created_rides",
        foreign_keys=[creator_id],
    )
    riders = db.relationship(
        "Rider",
        backref="ride",
    )

    def search(
        origin=None,
        destination=None,
        departure_date=None,
        tab=None,
        utc_offset=0,
    ):
        upcoming_rides = Ride.query_upcoming_rides()

        if tab == "from":
            upcoming_rides = upcoming_rides.where(
                Ride.origin == "Princeton"
            )

            if destination is not None and destination != "":
                upcoming_rides = upcoming_rides.where(
                    or_(
                        # Matches if the search term is a prefix of the
                        # destination
                        Ride.destination.ilike(f"%{destination}%"),
                        # Full text match with escaped user query
                        # (using custom PostgreSQL functions)
                        func.to_tsvector(Ride.destination).op("@@")(
                            func.plainto_tsquery(destination)
                        ),
                    )
                )

        elif tab == "to":
            upcoming_rides = upcoming_rides.where(
                Ride.destination == "Princeton"
            )

            if origin is not None and origin != "":
                upcoming_rides = upcoming_rides.where(
                    or_(
                        Ride.origin.ilike(f"%{origin}%"),
                        func.to_tsvector(Ride.origin).op("@@")(
                            func.plainto_tsquery(origin)
                        ),
                    )
                )

        if departure_date is not None and departure_date != "":
            # Get the datetimes which start and end the chosen day
            # from the date string
            midnight_start = datetime.strptime(
                departure_date, "%Y-%m-%d"
            )
            midnight_end = datetime.combine(
                midnight_start, datetime.max.time()
            )

            # Add UTC offset to account for local timezone differences
            delt = timedelta(minutes=int(utc_offset))

            upcoming_rides = upcoming_rides.where(
                Ride.departure_datetime >= midnight_start + delt,
                Ride.departure_datetime <= midnight_end + delt,
            )

        return upcoming_rides.all()

    def format_departure_datetime(self):
        return self.departure_datetime.strftime("%m-%d-%Y at %H:%M %p")

    def query_upcoming_rides():
        # Return appropriately ordered rides list
        return (
            Ride.query.where(
                Ride.departure_datetime >= ride_departure_limit()
            )
            .order_by(Ride.departure_datetime.asc())
            .order_by(Ride.destination.asc())
            .order_by(Ride.origin.asc())
        )

    def get_upcoming_rides():
        return Ride.query_upcoming_rides().all()

    def create_rider(self, user, is_creator=False):
        ride_id = self.id
        user_id = user.id
        return Rider(
            ride_id=ride_id, user_id=user_id, is_creator=is_creator
        ).save()

    def create_request(self, user):
        ride_id = self.id
        user_id = user.id
        return RideRequest(ride_id=ride_id, user_id=user_id).save()

    def get_creator(self):
        return self.creator

    def get_riders(self):
        return self.riders

    def get_all_requests(self):
        return self.requests

    def get_pending_requests(self):
        return RideRequest.query.where(
            RideRequest.ride_id == self.id,
            RideRequest.status == RideRequest.Status.PENDING.value,
        ).all()

    def get_accepted_requests(self):
        return RideRequest.query.where(
            RideRequest.ride_id == self.id,
            RideRequest.status == RideRequest.Status.ACCEPTED.value,
        ).all()

    def get_rejected_requests(self):
        return RideRequest.query.where(
            RideRequest.ride_id == self.id,
            RideRequest.status == RideRequest.Status.REJECTED.value,
        ).all()

    def riders_count(self):
        return len(self.riders)

    def is_full(self):
        return self.riders_count() >= self.capacity

    def has_room(self):
        return self.capacity > self.riders_count()

    def is_user_rider(self, user):
        return (
            Rider.query.where(
                Rider.ride_id == self.id, Rider.user_id == user.id
            ).first()
            is not None
        )

    def has_user_requested(self, user):
        return (
            RideRequest.query.where(
                RideRequest.ride_id == self.id,
                RideRequest.user_id == user.id,
            ).first()
            is not None
        )

    def is_user_creator(self, user):
        return self.creator_id == user.id

    def is_user_request_pending(self, user):
        return (
            RideRequest.query.where(
                RideRequest.ride_id == self.id,
                RideRequest.user_id == user.id,
                RideRequest.status == RideRequest.Status.PENDING.value,
            ).first()
            is not None
        )

    def has_user_been_rejected(self, user):
        return (
            RideRequest.query.where(
                RideRequest.ride_id == self.id,
                RideRequest.user_id == user.id,
                RideRequest.status == RideRequest.Status.REJECTED.value,
            ).first()
            is not None
        )

    def has_user_been_accepted(self, user):
        return (
            RideRequest.query.where(
                RideRequest.ride_id == self.id,
                RideRequest.user_id == user.id,
                RideRequest.status == RideRequest.Status.ACCEPTED.value,
            ).first()
            is not None
        )

    def has_user_cancelled(self, user):
        return (
            RideRequest.query.where(
                RideRequest.ride_id == self.id,
                RideRequest.user_id == user.id,
                RideRequest.status
                == RideRequest.Status.CANCELLED.value,
            ).first()
            is not None
        )

    def __repr__(self):
        return "<Ride from {} to {} on {}>".format(
            self.origin, self.destination, self.departure_datetime
        )


# Creator becomes rider after ride is created
@db.event.listens_for(Ride, "after_insert")
def after_insert(mapper, connection, target):
    rider_table = Rider.__table__
    if target.creator_id is not None:
        connection.execute(
            rider_table.insert(),
            {
                "ride_id": target.id,
                "user_id": target.creator_id,
                "is_creator": True,
            },
        )


class RideRequest(AbstractModel):
    __tablename__ = "ride_requests"

    class Status(enum.Enum):
        PENDING = 1
        ACCEPTED = 2
        REJECTED = 3
        CANCELLED = 4

    # Fields
    ride_id = db.Column(
        db.Integer,
        db.ForeignKey("rides.id"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    status = db.Column(
        db.Integer,
        nullable=False,
        default=Status.PENDING.value,
    )
    status_changed_at = db.Column(
        db.DateTime,
        index=True,
    )

    # Relationships to other tables
    user = db.relationship(
        "User",
        backref="outbound_requests",
        foreign_keys=[user_id],
    )
    ride = db.relationship(
        "Ride",
        backref="requests",
        foreign_keys=[ride_id],
    )

    def is_accepted(self):
        return self.status == self.Status.ACCEPTED.value

    def is_rejected(self):
        return self.status == self.Status.REJECTED.value

    def is_pending(self):
        return self.status == self.Status.PENDING.value

    def is_cancelled(self):
        return self.status == self.Status.CANCELLED.value

    def accept(self):
        if self.ride.is_full():
            return

        self.status = self.Status.ACCEPTED.value
        self.to_rider().save()
        self.status_changed_at = datetime.utcnow()
        self.save()

    def reject(self):
        self.status = self.Status.REJECTED.value
        Rider.query.where(
            Rider.ride_request_id == self.id,
            Rider.user_id == self.user_id,
        ).delete()
        self.status_changed_at = datetime.utcnow()
        self.save()

    def cancel(self):
        self.status = self.Status.CANCELLED.value
        self.status_changed_at = datetime.utcnow()
        self.save()

    def to_rider(self):
        return Rider(
            ride_request_id=self.id,
            ride_id=self.ride_id,
            user_id=self.user_id,
        )

    def __repr__(self):
        return "<[{}] Request from User:{} join Ride:{}>".format(
            self.status, self.user_id, self.ride_id
        )


class Rider(AbstractModel):
    __tablename__ = "riders"

    # Fields
    ride_request_id = db.Column(
        db.Integer,
        db.ForeignKey("ride_requests.id"),
        nullable=True,
    )
    ride_id = db.Column(
        db.Integer,
        db.ForeignKey("rides.id"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    is_creator = db.Column(
        db.Boolean,
        index=False,
        nullable=False,
        default=False,
    )

    # Relationships to other tables
    ride_request = db.relationship(
        "RideRequest",
        backref="rider",
        foreign_keys=[ride_request_id],
    )
    user = db.relationship(
        "User",
        backref="rider_instances",
        foreign_keys=[user_id],
    )

    def netid(self):
        return self.user.netid

    def remove(self):
        if self.ride_request_id is not None:
            db.session.delete(self.ride_request)
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Rider User:{} on Ride:{}>".format(
            self.user_id, self.ride_id
        )
