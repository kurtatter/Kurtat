from flask import Blueprint

bp = Blueprint('cabinet', __name__, template_folder='templates', url_prefix='/cabinet')

from app.cabinet import routes
