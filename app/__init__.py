# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db      = SQLAlchemy()
migrate = Migrate()
login   = LoginManager()

def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='../static',
        template_folder='../templates'
    )
    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY                  = os.getenv('SECRET_KEY', 'dev-secret'),
        SQLALCHEMY_DATABASE_URI     = 'sqlite:///' + os.path.join(app.instance_path, 'notes.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'

    # Make sure models are imported so SQLAlchemy knows about them
    from . import models

    # Register blueprints
    from .auth  import auth_bp
    from .notes import notes_bp
    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')

    return app   # <— this is critical!
# app/__init__.py

from flask_login import LoginManager

login = LoginManager()

# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db      = SQLAlchemy()
migrate = Migrate()
login   = LoginManager()

def create_app():
    # Create the app with the correct import name and folders
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder='../static',
        template_folder='../templates'
    )
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuration
    app.config.from_mapping(
        SECRET_KEY='dev-secret',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'notes.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'

    # Tell Flask-Login how to load a user from session
    @login.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    # Ensure models are registered
    from . import models

    # Register Blueprints
    from .auth import auth_bp
    from .notes import notes_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')

    return app


