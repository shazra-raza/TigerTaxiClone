"""Init module for the TigerTaxi server.

Defines the Flask application factory.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu),
Kwasi Oppong-Badu '22 (kyo@princeton.edu)
"""

# ----------------------------------------------------------------------

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, Response, redirect, request

from tigertaxi.blueprint import main_bp
from tigertaxi.errors import internal_error, not_found_error
from tigertaxi.extensions import cas, db, mail

# ----------------------------------------------------------------------


def create_app() -> Flask:
    """Application factory for TigerTaxi.

    Returns a Flask application instance configured with the environment
    variables, extensions, and routes necessary to serve the site.
    """

    app = Flask(__name__)

    # Configures the app based on the settings specified in
    # one of the Config objects
    app.config.from_object("config.ProductionConfig")

    # Flask extensions
    db.init_app(app)  # type: ignore[no-untyped-call]
    cas.init_app(app)
    mail.init_app(app)

    # Application routes
    app.register_blueprint(main_bp)

    # Error handlers
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)

    # Jinja2 rendering
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    if app.env == "production":

        def force_https() -> Response:
            """Redirects all incoming HTTP requests to their HTTPS
            equivalent.

            This function should only be registered as a request handler
            in a production environment such as Heroku. Forcing HTTPS in
            a local enviroment will typically cause the "invalid
            response" errors to be thrown from the browser.
            """
            if not request.is_secure:
                url = request.url.replace("http://", "https://", 1)
                return redirect(url, code=301)

        app.before_request(force_https)

    # Logging
    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/tigertaxi.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s "
                "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("TigerTaxi startup")

    return app
