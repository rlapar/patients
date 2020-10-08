from patients.dbmodels.settings import configure_dbmodels

from . import settings
from .logs import configure_structlog


configure_structlog()
configure_dbmodels(settings.db_url)


from .app import app