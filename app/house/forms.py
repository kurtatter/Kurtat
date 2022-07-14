from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    RadioField,
    Label,
    IntegerField,
    FloatField,
    FileField,
    MultipleFileField,
    TextAreaField
)


class AddHouseForm(FlaskForm):
    house_or_flat = RadioField('house_or_flat', choices=[('rbHouse', 'House'), ('rbFlat', 'Flat')])
    rooms = IntegerField('Numeric of rooms')
    beds = IntegerField('Numeric of beds')
    price = FloatField('Price')
    crowd = RadioField('Толпой вариант?', choices=[('yes', 'Да'), ('no', 'Нет')])
    noisy = RadioField('Шуметь вариант?', choices=[('yes', 'Да'), ('no', 'Нет')])
    images = MultipleFileField('Загрузить фотографии')
    description = TextAreaField('Описание')
    submit = SubmitField('Отправить')
