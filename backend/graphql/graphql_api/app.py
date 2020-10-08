import json

from flask import Flask, Response
from flask_graphql import GraphQLView

from . import middleware
from .api import schema
from .auth import auth_required
from .settings import endpoint_prefix


def health():
    return Response(json.dumps({"status": "pong"}), mimetype="application/json")


def create_app():
    app = Flask(__name__)
    # app.debug = settings.debug
    app.before_request(auth_required)
    app.before_request(middleware.before_request)
    app.after_request(middleware.after_request)

    app.add_url_rule(f"{endpoint_prefix}/ping", view_func=health)
    app.add_url_rule(
        f"{endpoint_prefix}",
        view_func=GraphQLView.as_view(
            "graphql",
            schema=schema,
            middleware=[middleware.ValidationMiddleware()],
            graphiql=True
        )
    )
    return app


app = create_app()
