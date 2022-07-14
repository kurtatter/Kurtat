from app.models import (
    Message,
    MessageStatus,
    Dialog,
    DialogType,
    dialogs,
    User
)
from app import db

from sqlalchemy import and_, text


class MessageService:
    @staticmethod
    def get_last_message(dialog):
        return Message.query.filter_by(dialog_id=dialog.id)\
            .order_by(-Message.send_datetime).first()

    @staticmethod
    def get_dialog_messages(dialog_id):
        return Message.query.filter_by(dialog_id=dialog_id).all()

    @staticmethod
    def sent_private_message(sender, recipient, text):
        recipient_dialogs = db.session.query(dialogs.c.dialog_id).join(Dialog,
                                                                       and_(Dialog.id == dialogs.c.dialog_id,
                                                                            Dialog.type == DialogType.private)) \
                                                                    .filter(dialogs.c.user_id == recipient.id).all()
        sender_dialogs = db.session.query(dialogs.c.dialog_id).join(Dialog,
                                                                    and_(Dialog.id == dialogs.c.dialog_id,
                                                                         Dialog.type == DialogType.private)) \
                                                                    .filter(dialogs.c.user_id == sender.id).all()
        our_dialog_id = (set(recipient_dialogs) & set(sender_dialogs)).pop()
        our_dialog_id = our_dialog_id[0] if our_dialog_id else None
        # print('our_dialog_id', our_dialog_id)
        if our_dialog_id:
            dialog = Dialog.query.get(our_dialog_id)
        else:
            dialog = Dialog.create_private_dialog(sender.id, recipient.id, DialogType.private)
            db.session.add(dialog)
            db.session.commit()
        message = Message(
            text=text,
            recipient_id=recipient.id,
            dialog_id=dialog.id,
            sender_id=sender.id
        )
        db.session.add(message)
        db.session.commit()
        return dialog.id

    @staticmethod
    def get_contact(user_id, dialog_id):
        contact_id = db.session.execute(
            text(f"select user_id from User_Dialog where user_id != {user_id} and dialog_id={dialog_id}")).first()[0]
        return User.query.get(contact_id)

    @staticmethod
    def all_messages_have_been_read(dialog_id, recipient_id):
        for message in Message.query.filter_by(dialog_id=dialog_id, recipient_id=recipient_id).all():
            if message.status == MessageStatus.on_the_way:
                message.status = MessageStatus.read
                db.session.add(message)
        db.session.commit()

    def on_the_way_messages_count(self, user_id):
        return Message.query.filter_by(status=MessageStatus.on_the_way, recipient_id=user_id).count()


class DialogService:
    @staticmethod
    def create_private_dialog(sender_id, recipient_id, dialog_type=DialogType.private):
        recipient_dialogs = db.session.query(dialogs.c.dialog_id).join(Dialog,
                                                                       and_(Dialog.id == dialogs.c.dialog_id,
                                                                            Dialog.type == DialogType.private)) \
            .filter(dialogs.c.user_id == recipient_id).all()
        sender_dialogs = db.session.query(dialogs.c.dialog_id).join(Dialog,
                                                                    and_(Dialog.id == dialogs.c.dialog_id,
                                                                         Dialog.type == DialogType.private)) \
            .filter(dialogs.c.user_id == sender_id).all()
        our_dialog_id = (set(recipient_dialogs) & set(sender_dialogs)).pop() if (set(recipient_dialogs) & set(sender_dialogs)) else None
        our_dialog_id = our_dialog_id[0] if our_dialog_id else None
        # print('our_dialog_id', our_dialog_id)
        if our_dialog_id:
            dialog = Dialog.query.get(our_dialog_id)
            return dialog
        else:
            new_dialog = Dialog(type=dialog_type)
            db.session.add(new_dialog)
            db.session.commit()
            try:
                db.engine.connect().execute(
                    dialogs.insert().values({'user_id': sender_id, 'dialog_id': new_dialog.id})
                )
                db.engine.connect().execute(
                    dialogs.insert().values({'user_id': recipient_id, 'dialog_id': new_dialog.id})
                )
                return new_dialog
            except Exception:
                db.session.delete(new_dialog)
                db.session.commit()