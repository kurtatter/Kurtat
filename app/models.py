from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import and_, text

from app import db, login

from datetime import datetime
import enum

"""
Отношения таблиц:
Диалог - Сообщение (Одни-ко-Многим)
Дилог - Пользователь (Многие-ко-Многим)
"""

dialogs = db.Table('User_Dialog',
                   db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                   db.Column('dialog_id', db.Integer, db.ForeignKey('Dialog.id'))
                   )


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(24))
    deleted = db.Column(db.Boolean, default=0)
    avatar = db.Column(db.String(240), nullable=True)
    dialogs = db.relationship('Dialog', secondary=dialogs, backref='users', lazy='dynamic')
    houses = db.relationship('House', backref='author', lazy='dynamic')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_avatar(self, avatar_number):
        self.avatar = f"https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-{avatar_number}.webp"

    @staticmethod
    def get_private_dialog_with(first_user, second_user):
        recipient_messages = Message.query.filter_by(recipient=first_user, sender=second_user).all()
        sender_messages = Message.query.filter_by(sender=first_user, recipient=second_user).all()
        print('recipient_messages', recipient_messages)
        print('sender_messages', sender_messages)
        if recipient_messages:
            for message in recipient_messages:
                if message and message.dialog.type == DialogType.private:
                    return message.dialog
        elif sender_messages:
            for message in sender_messages:
                if message and message.dialog.type == DialogType.private:
                    return message.dialog
        else:
            dialog = Dialog(type=DialogType.private)
            db.session.add(dialog)
            db.session.commit()
            return dialog

    # def create_private_dialog(self):
    #     dialogs =

    # def sent_private_message(self, text, recipient):
    #     recipient_dialogs = db.session.query(dialogs.c.dialog_id).join(Dialog,
    #                                                                    and_(Dialog.id == dialogs.c.dialog_id,
    #                                                                         Dialog.type == DialogType.private)) \
    #         .filter(dialogs.c.user_id == recipient.id).all()
    #     sender_dialogs = db.session.query(dialogs.c.dialog_id).join(Dialog,
    #                                                                 and_(Dialog.id == dialogs.c.dialog_id,
    #                                                                      Dialog.type == DialogType.private)) \
    #         .filter(dialogs.c.user_id == self.id).all()
    #     # print('recipient_dialogs', recipient_dialogs, set(recipient_dialogs))
    #     # print('sender_dialogs', sender_dialogs, set(sender_dialogs))
    #     our_dialog_id = (set(recipient_dialogs) & set(sender_dialogs)).pop()
    #     our_dialog_id = our_dialog_id[0] if our_dialog_id else None
    #     # print('our_dialog_id', our_dialog_id)
    #     if our_dialog_id:
    #         dialog = Dialog.query.get(our_dialog_id)
    #     else:
    #         dialog = Dialog.create_private_dialog(self.id, recipient.id, DialogType.private)
    #         db.session.add(dialog)
    #         db.session.commit()
    #     message = Message(
    #         text=text,
    #         recipient_id=recipient.id,
    #         dialog_id=dialog.id,
    #         sender_id=self.id
    #     )
    #     db.session.add(message)
    #     db.session.commit()
    #     return dialog.id

    def __repr__(self):
        return '<{}: {}>'.format(self.email, self.username)


@login.user_loader
def load_user(id: str):
    return User.query.get(int(id))


class House(db.Model):
    __tablename__ = 'House'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    price = db.Column(db.Float(precision=2), index=True)
    rooms = db.Column(db.Integer)
    beds = db.Column(db.Integer)
    is_crowd = db.Column(db.Boolean)
    is_noisy = db.Column(db.Boolean)
    description = db.Column(db.Text)
    longitude = db.Column(db.Float(precision=12))
    latitude = db.Column(db.Float(precision=12))
    mount_distance = db.Column(db.Float(3), index=True)
    water_distance = db.Column(db.Float(3), index=True)
    forest_distance = db.Column(db.Float(3), index=True)
    city_distance = db.Column(db.Float(3), index=True)
    deleted = db.Column(db.Boolean, default=0)

    images = db.relationship('HouseImages', backref='house', lazy='dynamic')


class HouseImages(db.Model):
    __tablename__ = 'HouseImage'

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.Text)
    house_id = db.Column(db.Integer, db.ForeignKey('House.id'))
    deleted = db.Column(db.Boolean, default=0)


class HousePublish(db.Model):
    __tablename__ = 'HousePublish'

    id = db.Column(db.Integer, primary_key=True)
    home_id = db.Column(db.Integer, db.ForeignKey('House.id'))
    publish_datetime = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    vip = db.Column(db.Boolean, default=0)
    deleted = db.Column(db.Integer, default=0)


class HouseComments(db.Model):
    __tablename__ = 'HouseComment'

    id = db.Column(db.Integer, primary_key=True)
    send_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'), index=True)
    sender = db.relationship('User', foreign_keys=sender_id)
    recipient_id = db.Column(db.Integer, db.ForeignKey('User.id'), index=True)
    recipient = db.relationship('User', foreign_keys=recipient_id)
    house_publish_id = db.Column(db.Integer, db.ForeignKey('HousePublish.id'))
    deleted = db.Column(db.Boolean, default=0)


class MessageStatus(enum.Enum):
    on_the_way = 0
    delivered = 1
    read = 2


class DialogType(enum.Enum):
    private = 0
    public = 1


class Dialog(db.Model):
    __tablename__ = 'Dialog'

    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='dialogs', lazy='dynamic')
    create_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.Enum(DialogType), default=DialogType.private)

    def create_private_dialog(your_id, him_id, dialog_type='private'):
        new_dialog = Dialog(type=dialog_type)
        db.session.add(new_dialog)
        db.session.commit()
        try:
            db.engine.connect().execute(
                dialogs.insert().values({'user_id': your_id, 'dialog_id': new_dialog.id})
            )
            db.engine.connect().execute(
                dialogs.insert().values({'user_id': him_id, 'dialog_id': new_dialog.id})
            )
            return new_dialog
        except Exception:
            db.session.delete(new_dialog)
            db.session.commit()

    def get_contact(self, user_id, dialog_id):
        contact_id = db.session.execute(
            text(f"select user_id from User_Dialog where user_id != {user_id} and dialog_id={dialog_id}")).first()[0]
        return User.query.get(contact_id)

    def on_the_way_messages_count(self, user_id):
        return self.messages.filter_by(status=MessageStatus.on_the_way, recipient_id=user_id).count()


class Message(db.Model):
    __tablename__ = 'Message'

    id = db.Column(db.Integer, primary_key=True)
    send_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('User.id'), index=True)
    sender = db.relationship('User', foreign_keys=sender_id)
    recipient_id = db.Column(db.Integer, db.ForeignKey('User.id'), index=True)
    recipient = db.relationship('User', foreign_keys=recipient_id)
    status = db.Column(db.Enum(MessageStatus), default=MessageStatus.on_the_way)
    dialog_id = db.Column(db.Integer, db.ForeignKey('Dialog.id'))
    deleted = db.Column(db.Boolean, default=0)
