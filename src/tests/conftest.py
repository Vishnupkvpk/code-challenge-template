import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()  # Pass the 'testing' configuration to create_app
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database():
    # Initialize the database if needed for the test setup
    db.create_all()

    yield db

    # Teardown actions if needed
    db.session.remove()
    db.drop_all()
