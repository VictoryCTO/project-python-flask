import os
from dotenv import load_dotenv


class Config:
    # SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
    # old: SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///users.db")
    SECRET_KEY = os.getenv("SECRET_KEY")
    # old:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///users.db")
    # new:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier testing
