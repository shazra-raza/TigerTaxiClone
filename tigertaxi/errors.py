"""Error-handling functions for TigerTaxi.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu),
Kwasi Oppong-Badu '22 (kyo@princeton.edu)
"""

# ----------------------------------------------------------------------

from typing import Any

from flask import Response, render_template

from tigertaxi.extensions import db

# ----------------------------------------------------------------------


def not_found_error(error: Any) -> tuple[Response, int]:
    """Error handler for HTTP 404 errors.

    Renders the 404 error page and returns it as a response.
    """
    return render_template("errors/404.html"), 404


def internal_error(error: Any) -> tuple[Response, int]:
    """Error handler for HTTP 500 errors.

    Rolls back the last change made in the database, then renders the
    500 error page and returns it as a response.
    """
    db.session.rollback()
    return render_template("errors/500.html"), 500
