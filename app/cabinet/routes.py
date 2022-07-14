from app.cabinet import bp
from app import db
from app.main.forms import EditProfileForm

from flask import redirect, render_template, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.house.forms import AddHouseForm
from app.models import House
from app.models import User
from flask import current_app
import os


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = EditProfileForm()
    if form.validate_on_submit():
        print("Tut")
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        avatar = form.avatar.data
        file_name = secure_filename(avatar.filename)
        avatar_save_path = os.path.join(os.getcwd(), 'app', 'cabinet', 'static', file_name)
        avatar.save(avatar_save_path)
        current_user.avatar = file_name
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('.index'))
    hf = AddHouseForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.phone_number.data = current_user.phone_number
    form.avatar.data = current_user.avatar
    form.username.disabled = True
    houses = current_user.houses.all()
    return render_template('cabinet.html', form=form, hf=hf, houses=houses)


@bp.route('/change', methods=['GET', 'POST'])
def change():
    form = EditProfileForm()

    if form.validate_on_submit():
        print("Tut")
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        file_name = secure_filename(form.avatar.filename)
        avatar_save_path = os.path.join(os.getcwd(), 'app', 'cabinet', 'static', file_name)
        form.avatar.save(avatar_save_path)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('.index'))
