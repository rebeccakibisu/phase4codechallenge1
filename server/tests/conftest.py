import pytest
from server.app import app as flask_app
from server.models import db as _db

@pytest.fixture(scope="session")
def test_app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()

@pytest.fixture()
def client(test_app):
    return test_app.test_client()

@pytest.fixture()
def db(test_app):
    with test_app.app_context():
        yield _db

@pytest.fixture()
def app(test_app):
    return test_app
