from flask import Blueprint

bp = Blueprint('cabinet', __name__, template_folder='templates', url_prefix='/cabinet', static_folder='static')

from app.cabinet import routes
