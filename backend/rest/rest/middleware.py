"""Custom middleware for flask."""

import uuid

import flask
import structlog

from patients.dbmodels.database import db_session

log = structlog.get_logger()


def logger():
    """Return a structlog logger object.

    The logger will have a request ID and some extra info bound to it.
    """
    request_id = str(uuid.uuid4())
    flask.g.request_id = request_id
    return log.new(request_id=request_id, url=flask.request.path)


def before_request():
    """Flask middleware handle for before each request."""
    flask.g.logger = logger()


def after_request(response):
    """Flask middleware handle for after each request."""
    db_session.remove()
    db_session.bind.pool.dispose()
    return response
