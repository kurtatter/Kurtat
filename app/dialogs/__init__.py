from flask import Blueprint

bp = Blueprint('dialogs', __name__,
               url_prefix='/dialogs',
               template_folder='templates',
               static_folder='static',
               static_url_path='/static/dialogs'
               )

from app.dialogs import routes
