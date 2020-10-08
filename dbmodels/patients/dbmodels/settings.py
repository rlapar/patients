import os

APP_NAME = os.getenv('APP_NAME', 'patients.dbmodels')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
DEBUG = os.getenv('DEBUG', False)

DB_URL = os.getenv('DB_URL', 'postgresql://localhost')


def configure_dbmodels(db_url):
    global DB_URL
    DB_URL = db_url
