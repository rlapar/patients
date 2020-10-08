import uuid

import flask
import structlog
import jsonschema

from patients.dbmodels.database import db_session

log = structlog.get_logger()


def logger():
    return log.new(request_id=str(uuid.uuid4()), url=flask.request.path, user=flask.g.username)


def before_request():
    flask.g.logger = logger()


def after_request(response):
    db_session.remove()
    db_session.bind.pool.dispose()
    return response


class ValidationMiddleware:
    validation_schema = {
        "type": "object",
        "properties": {
            "offset": {"minimum": 0, "type": "number"},
            "limit": {"minimum": 1, "maximum": 500, "type": "number"},
        },
    }

    def resolve(self, next, root, info, **args):
        self.validate(args)
        return next(root, info, **args)

    def validate(self, args):
        jsonschema.validate(instance=args, schema=self.validation_schema)
