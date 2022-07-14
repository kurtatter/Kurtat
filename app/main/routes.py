from app.main import bp
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Message, Dialog, User
from app.dialogs.forms import SendMessage
from app.models import House, HouseImages


@bp.route('/')
def index():
    houses = House.query.all()
    return render_template('index.html', houses=houses)



