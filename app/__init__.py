from flask import Flask
from .extensions import db, migrate, bcrypt
from .config import Config
from .routes import register_blueprints


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app
