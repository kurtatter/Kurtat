from app.house import bp
from flask import request, redirect, url_for, render_template
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.house.forms import AddHouseForm
from app.models import House, HouseImages
from app import db
import os


@bp.route('/house_list')
def house_list():
    ...


@bp.route('/add_house', methods=['GET', 'POST'])
def add_house():
    form = AddHouseForm()
    if form.validate_on_submit():
        house = House(
            user_id=current_user.id,
            price=form.price.data,
            rooms=form.rooms.data,
            beds=form.beds.data,
            is_crowd=True if form.crowd.data == 'yes' else False,
            is_noisy=True if form.noisy.data == 'yes' else False,
            description=form.description.data
        )
        db.session.add(house)
        db.session.commit()
        for image in form.images.data:
            file_name = secure_filename(image.filename)
            image_save_path = os.path.join(os.getcwd(), 'app', 'house', 'static/images', file_name)
            image.save(image_save_path)
            house_image = HouseImages(
                img_url=os.path.join('images', file_name),
                house_id=house.id
            )
            db.session.add(house_image)
        db.session.commit()

    return redirect(url_for('cabinet.index'))


@bp.route('/house-page/<int:house_id>')
def house_page(house_id):
    house = House.query.get(house_id)
    print('House author:', house.author)
    # dialog = current_user.get_private_dialog_with(house.author, current_user)
    # print('Private dialogs', dialog)
    return render_template('house.html', house=house)

