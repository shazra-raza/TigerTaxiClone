"""This file should contain records you want created when you run flask
db seed.

Example:
from yourapp.models import User

initial_user = {
    'username': 'superadmin'
}
if User.find_by_username(initial_user['username']) is None:
    User(**initial_user).save()

UNCOMMENT TO SEED YOUR DB
"""

# import random
# from datetime import datetime, timedelta

# from tigertaxi.models import Ride, RideRequest, User

# seeds = [
#     {
#         "netid": "kyo",
#         "email": "kyo@princeton.edu",
#         "disp_name": "Kwasi Oppong-Badu",
#     },
#     {
#         "netid": "muriithi",
#         "email": "muriithi@princeton.edu",
#         "disp_name": "Jude Muriithi",
#     },
#     {
#         "netid": "aatmikg",
#         "email": "aatmikg@princeton.edu",
#         "disp_name": "Aatmik Gupta",
#     },
#     {
#         "netid": "mvpatel",
#         "email": "mvpatel@princeton.edu",
#         "disp_name": "Meet Patel",
#     },
#     {
#         "netid": "sraza",
#         "email": "sraza@princeton.edu",
#         "disp_name": "Shazra Raza",
#     },
#     # "bb5943"
# ]

# for seed in seeds:
#     user = User.query.filter_by(netid=seed["netid"]).first()
#     if user is None:
#         u = User(**seed)
#         u.save()

# origins = ["A", "B", "C", "D"]
# destinations = ["A'", "B'", "C'", "D'"]

# for i in range(5):
#     Ride(
#         creator_id=1,  # set this to your index in seeds + 1
#         capacity=random.randint(2, 5),
#         origin=origins[random.randrange(len(origins))],
#         destination="Princeton",
#         departure_datetime=datetime.utcnow()
#         + timedelta(minutes=random.randrange(500, 500000)),
#         notes="",
#         is_anonymous=True,
#     ).save()

# for i in range(5):
#     Ride(
#         creator_id=1,  # set this to your index in seeds + 1
#         capacity=random.randint(2, 5),
#         origin="Princeton",
#         destination=destinations[random.randrange(len(destinations))],
#         departure_datetime=datetime.utcnow()
#         + timedelta(minutes=random.randrange(500, 500000)),
#         notes="",
#         is_anonymous=True,
#     ).save()

# for i in range(5):
#     Ride(
#         creator_id=random.randint(2, User.query.count()),
#         capacity=random.randint(2, 5),
#         origin=origins[random.randrange(len(origins))],
#         destination="Princeton",
#         departure_datetime=datetime.utcnow()
#         + timedelta(minutes=random.randrange(500, 500000)),
#         notes="",
#         is_anonymous=True,
#     ).save()

# for i in range(5):
#     Ride(
#         creator_id=random.randint(2, User.query.count()),
#         capacity=random.randint(2, 5),
#         origin="Princeton",
#         destination=destinations[random.randrange(len(destinations))],
#         departure_datetime=datetime.utcnow()
#         + timedelta(minutes=random.randrange(500, 500000)),
#         notes="",
#         is_anonymous=True,
#     ).save()

# for i in range(30):
#     ride = Ride.query.get(random.randint(1, Ride.query.count()))
#     user = User.query.get(random.randint(1, User.query.count()))
#     if ride.creator_id != user.id:
#         RideRequest(ride_id=ride.id, user_id=user.id).save()
