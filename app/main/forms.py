from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, FileField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone_number = StringField('Phone number')
    avatar = FileField('Avatar')
    save = SubmitField('Save')
