"""Page views for TigerTaxi.

Each view function in this module directly corresponds to a page
accessible on the site. The urls associated with each of these
functions are assigned in blueprint.py.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu),
Kwasi Oppong-Badu '22 (kyo@princeton.edu)
"""

# ----------------------------------------------------------------------

from flask import Response, make_response, render_template

from tigertaxi.extensions import cas
from tigertaxi.helpers import login_required
from tigertaxi.models import User

# ----------------------------------------------------------------------


def landing() -> Response:
    """Renders the landing page and returns it as a response."""
    return make_response(render_template("landing.html"))


def ride_guide() -> Response:
    """Renders the Ride Guide page and returns it as a response."""
    return make_response(render_template("guide.html"))


@login_required
def user_rides() -> Response:
    """Renders the My Rides page and returns it as a response."""
    user = User.query.filter_by(netid=cas.username).first_or_404()

    # Get user rides and requests by category
    created = user.get_created_rides()
    accepted = user.get_accepted_outbound_requests()
    pending = user.get_pending_outbound_requests()
    rejected = user.get_rejected_outbound_requests()

    html = render_template(
        "myrides.html",
        created=created,
        accepted=accepted,
        pending=pending,
        rejected=rejected,
        netid=cas.username,
    )
    return make_response(html)


@login_required
def settings() -> Response:
    """Renders the Settings page and returns it as a response."""
    user = User.query.filter_by(netid=cas.username).first_or_404()

    # Get user's current settings
    html = render_template(
        "settings.html",
        netid=cas.username,
        disp_name=user.disp_name,
        phone_number=user.phone_num,
        email_notifs=user.email_notifs,
    )
    return make_response(html)


@login_required
def search_rides() -> Response:
    """Renders the Search Rides page and returns it as a response."""
    return make_response(
        render_template("searchrides.html", netid=cas.username)
    )


@login_required
def create_ride() -> Response:
    """Renders the Create a Ride page and returns it as a response."""
    return make_response(
        render_template("createride.html", netid=cas.username)
    )
