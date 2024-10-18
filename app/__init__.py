from flask import Flask
from .extensions import db, migrate, bcrypt
from .config import Config
from .routes import register_blueprints
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    if config_class is None:
        config_class = (
            ProductionConfig
            if os.getenv("FLASK_ENV") == "production"
            else DevelopmentConfig
        )

    # Override the config class for testing
    if os.getenv("FLASK_ENV") == "testing":
        config_class = TestingConfig

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app
