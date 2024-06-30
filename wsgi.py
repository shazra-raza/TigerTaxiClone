# ----------------------------------------------------------------------
# wsgi.py
# Author: Jude Muriithi
# Description: Creates an app instance for use with gunicorn
# ----------------------------------------------------------------------
from tigertaxi import create_app

app = create_app()
