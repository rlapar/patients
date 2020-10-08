import connexion

from . import settings
from .auth import auth_required
from .middleware import before_request, after_request

def create_app():
    connexion_app = connexion.FlaskApp(__name__, specification_dir='swagger/')

    options = {
        'swagger_ui': True,
        'swagger_path': settings.SWAGGER_UI_DIR,
        'serve_spec': True,
        'strict_validation': True,
    }

    connexion_app.add_api(
        'patients.yml',
        options=options,
        strict_validation=True,
        arguments={'host': settings.host, 'schema': settings.schema, 'auth': settings.environment_label != 'test'},
    )

    flask_app=connexion_app.app
    flask_app.before_request(before_request)
    flask_app.before_request(auth_required)
    flask_app.after_request(after_request)

    return connexion_app

app = create_app()

