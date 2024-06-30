"""Central blueprint for TigerTaxi.

The blueprint object containing all application routes, as well as the
URLs of the routes themselves, are defined here.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu)
"""

# ----------------------------------------------------------------------

from typing import Any, Callable, List

from flask import Blueprint, Response

from tigertaxi import endpoints, pages

# ----------------------------------------------------------------------

main_bp = Blueprint("main_bp", __name__)


def url(
    url_rules: List[str],
    view_func: Callable[..., Response],
    **options: Any
) -> None:
    """Assigns all given url rules to the given view function, with any
    specified methods."""

    for url_rule in url_rules:
        main_bp.add_url_rule(url_rule, view_func=view_func, **options)


# Pages
url(["/landing"], pages.landing)
url(["/guide"], pages.ride_guide)
url(["/account/rides"], pages.user_rides)
url(["/account/settings"], pages.settings)
url(["/search", "/home", "/index", "/"], pages.search_rides)
url(["/rides/new"], pages.create_ride)

# Endpoints
url(["/user_logout"], endpoints.clear_session)
url(
    ["/users/<string:net_id>/update"],
    endpoints.user_update,
    methods=["POST"],
)
url(
    ["/rides"],
    endpoints.rides,
    methods=["GET", "POST"],
)
url(
    ["/rides/<string:ride_id>/leave"],
    endpoints.leave_ride,
    methods=["POST"],
)
url(
    ["/rides/<string:ride_id>/requests"],
    endpoints.ride_requests,
    methods=["POST"],
)
url(
    ["/ride_requests/<string:ride_req_id>/accept"],
    endpoints.ride_request_accept,
    methods=["POST"],
)
url(
    ["/ride_requests/<string:ride_req_id>/reject"],
    endpoints.ride_request_reject,
    methods=["POST"],
)
url(
    ["/ride_requests/<string:ride_req_id>/cancel"],
    endpoints.ride_request_cancel,
    methods=["POST"],
)
url(
    ["/riders/<string:rider_id>/remove"],
    endpoints.remove_rider,
    methods=["POST"],
)
