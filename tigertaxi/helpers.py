"""Helper functions for TigerTaxi.

Functions which are used across multiple files in the application and
functions which have no natural place in another file are defined here.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu)
"""

# ----------------------------------------------------------------------

from functools import wraps
from typing import Any, Callable

from flask import Response, flash, redirect, request, session, url_for

from tigertaxi.extensions import cas
from tigertaxi.models import User

# ----------------------------------------------------------------------


def login_required(
    function: Callable[..., Response]
) -> Callable[..., Response]:
    """Custom decorator to check user authentication on authenticated
    pages.

    Sends user to the landing page if they are not logged in. On
    successful CAS login, the user is added to the database if they
    don't already exist, and any relevant reminders for the user are
    flashed.
    """

    @wraps(function)
    def wrap(*args: Any, **kwargs: Any) -> Response:
        if "CAS_USERNAME" not in session:
            session["CAS_AFTER_LOGIN_SESSION_URL"] = (
                request.script_root + request.full_path
            )
            return redirect(url_for("main_bp.landing"))

        else:
            # Uses a custom session variable to check if we have a user
            # in the database (faster than just querying every time)
            if "TT_USER_EXISTS" not in session:
                user = User.query.filter_by(netid=cas.username).first()

                if user is None:
                    user = User(
                        netid=cas.username,
                        email=cas.attributes["cas:mail"],
                        disp_name=cas.attributes["cas:displayname"],
                    )
                    user.save()

                # Flash phone number reminder
                if user.phone_num is None:
                    flash(
                        "It's easier to coordinate rides over text. "
                        "We recommend adding your phone number in "
                        "'Settings'",
                        "warning",
                    )

                session["TT_USER_EXISTS"] = True

            return function(*args, **kwargs)

    return wrap
