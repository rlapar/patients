from flask import request, g, Response

from . import settings

def check_auth(username, password):
    """Check if a username password combination is valid."""
    # password_hash = hashlib.sha512(password.encode()).hexdigest()
    # if username == settings.username and password_hash == settings.password_hash:
    #     return True
    # return False

    # for testing purposes doing plaintext password
    if username == settings.username and password == settings.password:
        return True
    return False

def authenticate():
    """Send a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def basic_auth():
    auth = request.authorization
    if not check_auth(auth.username, auth.password):
        return authenticate()
    g.username = auth.username
    return None


def auth_required():
    if settings.testing_environment:
        return
    if request.path == "/rest/ping":
        return
    auth = request.headers.get("Authorization")
    if not auth:
        return authenticate()
    if auth.startswith("Basic"):
        return basic_auth()
    # unknown auth
    return authenticate()
