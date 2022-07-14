from app import create_app, db
from app.models import User, Message, Dialog, dialogs

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Message': Message, 'User': User, 'Dialog': Dialog, 'dialogs': dialogs}
# if __name__ == '__main__':
#     app.run()
