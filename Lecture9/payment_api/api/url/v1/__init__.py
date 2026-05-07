from flask import Blueprint

v1 = Blueprint('url_v1', __name__, url_prefix='/api/v1')

from . import payments
