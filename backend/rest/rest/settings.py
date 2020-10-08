import os

# -- CONSTANTS --
SWAGGER_UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger_ui')

# -- ENV VARS --
app_name = os.environ.get("APP_NAME", "patients_rest")
environment_label = os.getenv('ENVIRONMENT', 'local')
debug = os.getenv('DEBUG', False)
testing_environment = os.getenv('TESTING_ENVIRONMENT', False)

db_url = os.getenv('DB_URL', 'postgresql://localhost')

username = os.getenv('BASIC_AUTH_USERNAME')
password = os.getenv('BASIC_AUTH_PASSWORD')


def configure(environment):
    # default == test
    host = '127.0.0.1:8081'
    schema = 'http'

    if environment == 'local':
        host = '127.0.0.1:8081'
        schema = 'http'
    elif environment == 'dev':
        host = ''  # TODO
        schema = ''  # TODO
    elif environment == 'prod':
        host = '' #TODO
        schema = '' #TODO

    return (
        host,
        schema
    )


host, schema = configure(environment_label)


