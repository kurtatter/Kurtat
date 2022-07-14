from flask import Blueprint
import os

# STATIC_FOLDER = os.path.join(os.path.dirname(__file__), "static")
# TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "templates")

bp = Blueprint('house', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='/static/house'
               )

from app.house import routes
