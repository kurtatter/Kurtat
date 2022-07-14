from app.cabinet import bp
from app.main.forms import EditProfileForm

from flask import render_template
from flask_login import login_required, current_user

from app.house.forms import AddHouseForm
from app.models import House
from app.models import User
from flask import current_app


@bp.route('/')
def index():
    form = EditProfileForm()
    hf = AddHouseForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.phone_number.data = current_user.phone_number
    form.avatar.data = current_user.avatar
    form.username.disabled = True
    houses = current_user.houses.all()
    return render_template('cabinet.html', form=form, hf=hf, houses=houses)
