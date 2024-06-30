"""Flask extensions for TigerTaxi.

Defines global objects which point to the extensions, allowing them to
be imported and used across multiple files in the TigerTaxi package.

Contributors:
Jude Muriithi '24 (muriithi@princeton.edu)
"""

# ----------------------------------------------------------------------

from flask_cas import CAS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# ----------------------------------------------------------------------

cas = CAS()
db = SQLAlchemy()
mail = Mail()
