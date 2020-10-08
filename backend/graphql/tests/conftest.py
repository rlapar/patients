from mock import MagicMock
import pytest

from graphql_api.app import create_app
from graphql_api.middleware import ValidationMiddleware

APP = create_app()


def comparable_magic_mock():
    magic_mock = MagicMock()
    magic_mock.__le__ = MagicMock()
    magic_mock.__ge__ = MagicMock()
    magic_mock.__lt__ = MagicMock()
    magic_mock.__gt__ = MagicMock()
    return magic_mock


class ModelMock(object):
    created = comparable_magic_mock()
    updated = comparable_magic_mock()


@pytest.fixture(autouse=True, scope='session')
def app_context():
    context = APP.app_context()
    context.g.logger = MagicMock()
    context.g.username = 'test'
    context.push()

    yield

    context.pop()


@pytest.fixture
def app():
    return APP


@pytest.fixture(scope='session')
def validator(middleware=ValidationMiddleware()):
    return middleware


@pytest.fixture
def patch_type(mocker):
    def _patch(obj, type_name):
        mock_query = mocker.MagicMock(name='query')
        mock_type = mocker.patch.object(obj, type_name)
        mock_type.query = mock_query
        return mock_type

    return _patch


@pytest.fixture
def model():
    return ModelMock()
