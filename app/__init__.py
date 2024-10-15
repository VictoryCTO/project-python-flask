from flask import Flask
from .extensions import db, migrate, bcrypt
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Import models
    from .models import User, UserActiveStatusChange

    # Register blueprints
    from .routes import register_blueprints

    register_blueprints(app)

    return app
