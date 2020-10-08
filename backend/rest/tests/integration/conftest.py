import pytest

from rest import app as connexion_app


@pytest.fixture
def app():
    flask_app = connexion_app.app
    return flask_app
