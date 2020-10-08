import flask


def ping():
    """Return a response saying ``{"pong": true}``.

    This is useful for testing and health checks.
    """
    flask.g.logger.info('pinged', ponging=True)
    return {"status": "pong"}
