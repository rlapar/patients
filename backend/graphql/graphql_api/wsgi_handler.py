from graphql_api import app
import serverless_wsgi


def handle(event, context):
    return serverless_wsgi.handle_request(app.app, event, context)
