import pytest
from app import create_app
from app.extensions import db
from app.config import TestingConfig


@pytest.fixture
def app():
    # Create the app with the testing configuration
    app = create_app(config_class=TestingConfig)

    with app.app_context():
        db.create_all()  # Create tables

    yield app

    # Teardown: Clean up the database after each test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()  # Flask test client to send requests
