from alembic import command
from alembic.config import Config
import pytest

from patients.dbmodels.database import db_engine
from patients.dbmodels.models import Base


alembic_cfg = Config()
alembic_cfg.set_main_option('script_location', 'alembic')


@pytest.fixture(autouse=True)
def flush_db():
    db_engine.execute('drop schema if exists public cascade')
    db_engine.execute('create schema public')
    yield
    db_engine.execute('drop schema public cascade')


def test_upgrade():
    command.upgrade(alembic_cfg, 'head')


def test_upgrade_downgrade_upgrade():
    command.upgrade(alembic_cfg, 'head')
    command.downgrade(alembic_cfg, '-1')
    command.upgrade(alembic_cfg, 'head')


def test_create():
    Base.metadata.create_all(db_engine)
