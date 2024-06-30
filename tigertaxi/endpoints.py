"""Backend API views for TigerTaxi.

Each view function in this module is used to handle background requests
initiated by the frontend client, such as AJAX requests and form
submissions. The urls associated with each of these
functions are assigned in blueprint.py.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu),
Kwasi Oppong-Badu '22 (kyo@princeton.edu)
"""

# ----------------------------------------------------------------------

from datetime import datetime, timedelta
from html import escape
from re import compile

from flask import (
    Response,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_mail import Message

from tigertaxi.extensions import cas, mail
from tigertaxi.helpers import login_required
from tigertaxi.models import Ride, Rider, RideRequest, User

# ----------------------------------------------------------------------


def clear_session() -> Response:
    """Clears user session after CAS logout.

    Users should be redirected to this function after logging out of
    CAS, as determined by the CAS_AFTER_LOGOUT environment variable. If
    this does not occur, users could potentially access the site without
    having an entry in the database, resulting in broken UI and a 404 or
    500 error at the first SQLAlchemy User query.
    """

    session.clear()
    return redirect(url_for("main_bp.landing"))


# ------- User Controller -----------------------------------------------


@login_required
def user_update(net_id: str) -> Response:
    """Endpoint for updating user-adjustable settings.

    When a user submits a form on the Settings page, this function is
    called to handle the submitted form.
    """

    if cas.username != net_id:
        flash(
            "Your do not have permission to make this change!", "danger"
        )
        return redirect(request.referrer)

    user = User.query.filter_by(netid=net_id).first_or_404()

    if "disp_name" in request.form:
        name = request.form["disp_name"]
        if len(name) == 0:
            flash("Display name too short", "danger")
        elif len(name) > 256:
            flash("Display name too long", "danger")
        else:
            user.disp_name = name
            flash("Your display name has been changed!", "success")

    elif "phone_num" in request.form:
        num = request.form["phone_num"]

        # Same regex used for validating phone numbers in settings.js
        phone_regex = compile(
            "^\\+?([0-2]{1})?((-?)|(.?)|("
            " ?))\\(?[0-9]{3}\\)?((-?)|(.?)|( ?))[0-9]{3}((-?)|(.?)|("
            " ?))[0-9]{4}$"
        )

        if not phone_regex.match(num):
            flash("Invalid phone number format", "danger")
        elif len(num) > 16:
            flash("Phone number is too long", "danger")
        else:
            user.phone_num = num
            flash("Your phone number has been changed!", "success")

    elif "email_notifs" in request.form:
        value = request.form["email_notifs"]

        if value == "Yes":
            user.email_notifs = True
            flash(
                "Your email preferences have been changed!", "success"
            )
        elif value == "No":
            user.email_notifs = False
            flash(
                "Your email preferences have been changed!", "success"
            )
        else:
            flash("Invalid email preference value", "danger")

    user.save()

    return redirect(request.referrer)


# ------- Rides Controller ----------------------------------------------


# TODO potentially split into rides/search and rides/create
# TODO refactor this function and Ride.search to remove all
# form-specific handling in models.py
@login_required
def rides() -> Response:
    """Endpoint for ride search and creation.

    GET requests are used to look up rides based on query parameters.
    When a user searches for rides on the Search Rides page, AJAX
    requests are sent to this endpoint, and rendered HTML for the search
    results is returned. See static/js/searchrides.js and models.py for
    more information about the specific query parameters used in search
    and how they are handled.

    POST requests are used to create rides. When a user submits the form
    on the Create a Ride page, this endpoint is called to handle their
    form submission. Form fields are validated manually within this
    function. If the submitted form passes validation, the ride creator
    is notified based on their settings, and a success message is
    flashed.
    """
    if request.method == "GET":
        # Pulls params from url query strings
        params = request.args

        rides = Ride.search(**params)
        user = User.query.filter_by(netid=cas.username).first_or_404()
        html = render_template(
            "elements/ride_search_cards.html",
            rides=rides,
            current_user=user,
        )
        return make_response(html)

    elif request.method == "POST" and request.form is not None:
        # Get user from database
        user = User.query.filter_by(netid=cas.username).first_or_404()

        # Validate to/from
        to_from = request.form["to_from"]
        if not (to_from == "From" or to_from == "To"):
            flash("Invalid value for 'To/From Princeton'", "danger")
            return redirect(request.referrer)

        # Validate location
        location = request.form["location"]
        if len(location) == 0:
            flash("Location name is too short", "danger")
            return redirect(request.referrer)

        if len(location) > 256:
            flash("Location name is too long", "danger")
            return redirect(request.referrer)

        if location == "Princeton":
            flash(
                "'Princeton' is not a valid secondary location",
                "danger",
            )
            return redirect(request.referrer)

        # Validate date

        # Convert departure date/time from local to UTC
        delt = timedelta(minutes=int(request.form["utc_offset"]))
        date = (
            datetime.strptime(
                request.form["departure_datetime"], "%Y-%m-%dT%H:%M"
            )
            + delt
        )

        timediff = date - datetime.utcnow()
        if timediff <= timedelta(minutes=55) or timediff >= timedelta(
            days=182
        ):
            flash(
                "Rides must depart between one hour and six months "
                "from the current time",
                "danger",
            )
            return redirect(request.referrer)

        # Validate capacity
        capacity = int(request.form["capacity"])
        if capacity < 2 or capacity > 10:
            flash("Invalid ride capacity", "danger")
            return redirect(request.referrer)

        # Validate notes
        notes = request.form["notes"]
        if len(notes) > 280:
            flash("Ride notes are too long", "danger")
            return redirect(request.referrer)

        # Validate anonymity boolean
        show_id = request.form["show_id"]
        if not (show_id == "Yes" or show_id == "No"):
            flash(
                "Invalid value for 'Show my name and netid'", "danger"
            )
            return redirect(request.referrer)
        is_anonymous = False if show_id == "Yes" else True

        # Set ride to/from based on form
        origin = None
        destination = None

        if to_from == "From":
            destination = location
        else:
            origin = location

        ride = Ride(
            origin=origin,
            destination=destination,
            departure_datetime=date,
            capacity=capacity,
            notes=notes,
            is_anonymous=is_anonymous,
            creator_id=user.id,
        )
        ride.save()

        # Email notif upon creation
        if user.email_notifs:
            notif = Message(
                subject=(
                    "Your ride from {} to {} has been created.".format(
                        escape(ride.origin), escape(ride.destination)
                    )
                ),
                html=(
                    """
                    <style>p {{margin-bottom: 2rem;}}</style>
                    <p>Hello {},</p>
                    <p>Your ride can now be seen and requested by other
                    TigerTaxi users. <a href=\"{}\">Click here</a> to
                    manage the ride.</p>
                    <p>All the best,</p>
                    <p>TigerTaxi Team</p>
                    """
                ).format(
                    escape(user.disp_name),
                    url_for(
                        "main_bp.user_rides",
                        _external=True,
                        _scheme="https",
                    ),
                ),
                recipients=[user.email],
            )
            mail.send(notif)

        # Redirect to My Rides page
        flash("Your ride has been created!", "success")
        return redirect(url_for("main_bp.user_rides"))


@login_required
def leave_ride(ride_id: str) -> Response:
    """Endpoint for an accepted rider leaving a ride.

    When a user takes the "Leave Ride" action from the Accepted Rides
    tab of the My Rides page, this endpoint is called to handle the
    resulting form submission. Once a rider successfully leaves a ride,
    the ride creator is notified according to their settings, and a
    success message is flashed.
    """

    ride = Ride.query.filter_by(id=ride_id).first_or_404()
    current_user = User.query.filter_by(
        netid=cas.username
    ).first_or_404()
    rider = Rider.query.where(
        Rider.ride_id == ride_id, Rider.user_id == current_user.id
    ).first()

    if rider is None:
        flash(
            "You do not have permission to remove this rider!",
            "danger",
        )
        return redirect(request.referrer)

    else:
        rider_user = rider.user
        rider_name = rider_user.disp_name
        rider.remove()
        flash("You have successfully left the ride!", "success")
        if ride.creator.email_notifs:
            notif = Message(
                subject="{} has left your ride".format(
                    escape(rider_name)
                ),
                html=(
                    """
                    <style>p {{margin-bottom: 2rem;}}</style>
                    <p>Hello {},</p>
                    <p>{} has left your ride from {} to {} on {}.
                    <a href=\"{}\">Click here</a> to manage
                    your ride.</p>
                    <p>All the best,</p>
                    <p>TigerTaxi Team</p>
                    """
                ).format(
                    escape(ride.creator.disp_name),
                    escape(rider_name),
                    escape(ride.origin),
                    escape(ride.destination),
                    escape(ride.format_departure_datetime()),
                    url_for(
                        "main_bp.user_rides",
                        _external=True,
                        _scheme="https",
                    ),
                ),
                recipients=[ride.creator.email],
            )
            mail.send(notif)

        return redirect(request.referrer)


# --------- RideRequests controller ------------------------------------


@login_required
def ride_requests(ride_id: str) -> Response:
    """Endpoint for creating a ride request.

    When a user takes the "Request to Join" action from the Search Rides
    page, this function is called to handle the resulting form
    submission. Once a user successfully joins a ride, the ride's
    creator is notified according to their settings, and a success
    message is flashed.
    """

    user = User.query.filter_by(netid=cas.username).first_or_404()
    ride = Ride.query.filter_by(id=ride_id).first_or_404()

    if ride.is_user_rider(user):
        flash("You are already in this ride!", "danger")

    elif ride.is_full():
        flash(
            "This ride is full! No more requests can be made.", "danger"
        )

    else:
        ride_request = RideRequest(user_id=user.id, ride_id=ride.id)
        ride_request.save()

        if ride.creator.email_notifs:
            notif = Message(
                subject="New ride request from {}".format(
                    escape(user.disp_name)
                ),
                html=(
                    """
                    <style>p {{margin-bottom: 2rem;}}</style>
                    <p>Hello {},</p>
                    <p>You've received a ride request for
                    your ride from {} to {} on {}. <a href=\"{}\">
                    Click here</a> to manage the request.</p>
                    <p>All the best,</p>
                    <p>TigerTaxi Team</p>
                    """
                ).format(
                    escape(ride.creator.disp_name),
                    escape(ride.origin),
                    escape(ride.destination),
                    escape(ride.format_departure_datetime()),
                    url_for(
                        "main_bp.user_rides",
                        _external=True,
                        _scheme="https",
                    ),
                ),
                recipients=[ride.creator.email],
            )
            mail.send(notif)

        flash(
            "You have successfully requested to join the ride!",
            "success",
        )

    return redirect(request.referrer)


@login_required
def ride_request_accept(ride_req_id: str) -> Response:
    """Endpoint for accepting a ride request.

    When a user chooses to accept a ride request from the Created Rides
    tab of the My Rides page, this function is called to handle the
    resulting form submission. Once a ride request is accepted, the user
    who made the request is notified according to their settings and a
    success message is flashed to the ride creator.
    """

    ride_req = RideRequest.query.filter_by(
        id=ride_req_id
    ).first_or_404()
    ride = ride_req.ride

    if ride.creator.netid != cas.username:
        flash(
            "You do not have permission to accept this request!",
            "danger",
        )

    elif ride.is_full():
        flash(
            "This ride is full! Remove existing riders if you wish "
            "to accept requests.",
            "danger",
        )

    elif not ride_req.is_pending():
        flash(
            "This request has already been accepted, rejected, or "
            "cancelled!",
            "danger",
        )

    else:
        if ride_req.user.email_notifs:
            notif = Message(
                subject="{} has accepted your ride request".format(
                    escape(ride.creator.disp_name)
                ),
                html=(
                    """
                    <style>p {{margin-bottom: 2rem;}}</style>
                    <p>Hello {},</p>
                    <p>You've been accepted to ride from {} to {} on {}.
                    <a href=\"{}\">Click here</a> to manage
                    your accepted request.</p>
                    <p>All the best,</p>
                    <p>TigerTaxi Team</p>
                    """
                ).format(
                    escape(ride_req.user.disp_name),
                    escape(ride.origin),
                    escape(ride.destination),
                    escape(ride.format_departure_datetime()),
                    url_for(
                        "main_bp.user_rides",
                        _external=True,
                        _scheme="https",
                    ),
                ),
                recipients=[ride_req.user.email],
            )
            mail.send(notif)

        ride_req.accept()
        flash("You have successfully accepted the request!", "success")

    return redirect(request.referrer)


@login_required
def ride_request_reject(ride_req_id: str) -> Response:
    """Endpoint for rejecting a ride request.

    When a user chooses to reject a ride request from the Created Rides
    tab of the My Rides page, this function is called to handle the
    resulting form submission. Once a ride request is rejected, the user
    who made the request is notified according to their settings and a
    success message is flashed to the ride creator.
    """

    ride_req = RideRequest.query.filter_by(
        id=ride_req_id
    ).first_or_404()
    ride = ride_req.ride

    if ride.creator.netid != cas.username:
        flash(
            "You do not have permission to reject this request!",
            "danger",
        )

    elif not ride_req.is_pending():
        flash(
            "This request has already been accepted, rejected, or "
            "cancelled!",
            "danger",
        )

    else:
        if ride_req.user.email_notifs:
            notif = Message(
                subject="{} has rejected your ride request".format(
                    escape(ride.creator.disp_name)
                ),
                html=(
                    """
                    <style>p {{margin-bottom: 2rem;}}</style>
                    <p>Hello {},</p>
                    <p>Your request to ride from {} to {} on {}
                    has been rejected. <a href=\"{}\">Click here</a>
                    to look for other options.</p>
                    <p>All the best,</p>
                    <p>TigerTaxi Team</p>
                    """
                ).format(
                    escape(ride_req.user.disp_name),
                    escape(ride.origin),
                    escape(ride.destination),
                    escape(ride.format_departure_datetime()),
                    url_for(
                        "main_bp.search_rides",
                        _external=True,
                        _scheme="https",
                    ),
                ),
                recipients=[ride_req.user.email],
            )
            mail.send(notif)

        ride_req.reject()
        flash("You have successfully rejected the request!", "success")

    return redirect(request.referrer)


@login_required
def ride_request_cancel(ride_req_id: str) -> Response:
    """Endpoint for cancelling a pending ride request.

    When a user takes the "Cancel Request" action from the Pending
    Requests tab of the My Rides page, this function is called to handle
    the resulting form submission. Once a user successfully cancels a
    request, a success message is flashed.
    """

    ride_req = RideRequest.query.filter_by(
        id=ride_req_id
    ).first_or_404()

    if ride_req.user.netid != cas.username:
        flash(
            "You do not have permission to cancel this request!",
            "danger",
        )

    elif not ride_req.is_pending():
        flash(
            "This request has already been accepted, rejected, or "
            "cancelled!",
            "danger",
        )

    else:
        ride_req.cancel()
        flash("You have successfully cancelled the request!", "success")

    return redirect(request.referrer)


# --------- Riders controller ------------------------------------


@login_required
def remove_rider(rider_id: str) -> Response:
    """Endpoint for removing a rider from a ride.

    When a user takes the "Remove from Ride" action from the Created
    Rides tab of the My Rides page, this function is called to handle
    the resulting form submission. Once a rider is removed, the rider is
    notified according to their settings and a success message is
    flashed to the ride creator.
    """
    if request.method == "POST":
        rider = Rider.query.filter_by(id=rider_id).first_or_404()
        current_user = User.query.filter_by(
            netid=cas.username
        ).first_or_404()

        # Pointers used to maintain references to deleted objects
        rider_user = rider.user
        rider_name = rider_user.disp_name
        ride = rider.ride
        ride_creator = ride.creator

        if not current_user.netid == ride_creator.netid:
            flash(
                "You do not have permission to remove this rider!",
                "danger",
            )
        else:
            rider.remove()
            flash(
                f"You have successfully removed {rider_name} from the"
                " ride!",
                "success",
            )

            if rider.user.email_notifs:
                notif = Message(
                    subject=(
                        "{} has removed you from their ride".format(
                            current_user.disp_name
                        )
                    ),
                    html=(
                        """
                    <style>p {{margin-bottom: 2rem;}}</style>
                    <p>Hello {},</p>
                    <p>{} has removed you from their ride from {} to {}
                    on {}. <a href=\"{}\">Click here</a> to search for
                    other options.</p>
                    <p>All the best,</p>
                    <p>TigerTaxi Team</p>
                    """
                    ).format(
                        escape(rider_name),
                        escape(ride.creator.disp_name),
                        escape(ride.origin),
                        escape(ride.destination),
                        escape(ride.format_departure_datetime()),
                        url_for(
                            "main_bp.search_rides",
                            _external=True,
                            _scheme="https",
                        ),
                    ),
                    recipients=[rider.user.email],
                )
                mail.send(notif)

        return redirect(request.referrer)
