from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

# app = Flask(__name__)
# app.config.from_object(Config)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.cabinet import bp as cabinet_bp
    app.register_blueprint(cabinet_bp)

    from app.house import bp as house_bp
    app.register_blueprint(house_bp)

    from app.dialogs import bp as dialogs_bp
    app.register_blueprint(dialogs_bp)

    return app
