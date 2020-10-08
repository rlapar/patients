import os

# -- CONSTANTS --
endpoint_prefix = '/graphql'

# -- ENV VARS --
app_name = os.environ.get("APP_NAME", "patients_graphql")
environment_label = os.getenv('ENVIRONMENT', 'local')
debug = os.getenv('DEBUG', False)
testing_environment = os.getenv('TESTING_ENVIRONMENT', False)

db_url = os.getenv('DB_URL', 'postgresql://localhost')

username = os.getenv('BASIC_AUTH_USERNAME')
password = os.getenv('BASIC_AUTH_PASSWORD')
