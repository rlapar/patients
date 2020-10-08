from patients.dbmodels import settings

settings.DB_URL = 'postgresql://localhost'

try:
    from conftest_local import *
except ImportError:
    pass
