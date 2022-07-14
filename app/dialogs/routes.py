from app.dialogs import bp
from app.dialogs.services import MessageService, DialogService
from app.dialogs.forms import SendMessage

from flask import (
    render_template,
    redirect,
    url_for,
)
from flask_login import (
    login_required,
    current_user,
)


message_service = MessageService()


@login_required
@bp.route('/')
def index():
    data = {
        'dialogs': current_user.dialogs.all() if not current_user.is_anonymous else None,
        'last_message': message_service.get_last_message
    }
    return render_template('dialogs.html', data=data)


@login_required
@bp.route('/write_message/<sender_id>/<recipient_id>')
def write_message(sender_id, recipient_id):
    new_dialog = DialogService.create_private_dialog(sender_id, recipient_id)
    return redirect(url_for('.dialog', dialog_id=new_dialog.id))


@login_required
@bp.route('/dialog/<dialog_id>', methods=['GET', 'POST'])
def dialog(dialog_id):
    print('dialog', dialog_id)
    data = {}
    if dialog_id:
        MessageService.all_messages_have_been_read(dialog_id, current_user.id)
        data.update({
            'messages': message_service.get_dialog_messages(dialog_id),
            'last_message': message_service.get_last_message
        })
    form = SendMessage()
    data.update({
        'form': form,
        'dialogs': current_user.dialogs.all() if not current_user.is_anonymous else None
    })
    if form.validate_on_submit():
        message_service.sent_private_message(
            sender=current_user,
            recipient=message_service.get_contact(current_user.id, dialog_id),
            text=form.message.data
        )
        return redirect(url_for('.dialog', dialog_id=dialog_id))
    return render_template('dialogs.html', data=data)
