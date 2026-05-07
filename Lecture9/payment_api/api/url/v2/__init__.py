from flask import Blueprint

v2 = Blueprint('url_v2', __name__, url_prefix='/api/v2')

from . import payments
