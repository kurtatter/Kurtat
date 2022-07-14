from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, flash, request, render_template
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db

import os


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash(f'User: {form.username.data}, Password: {form.password.data}, remember: {form.remember_me.data}')
        return redirect(next_page)
    return render_template('login.html', form=form, title='Sign In')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        avatar = form.avatar.data
        file_name = secure_filename(avatar.filename)
        avatar_save_path = os.path.join(os.getcwd(), 'app', 'cabinet', 'static', file_name)
        avatar.save(avatar_save_path)
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data if form.phone_number.data else '',
            avatar=file_name
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
