import pytest

from sqlalchemy.exc import IntegrityError

from patients.dbmodels.database import db_session, db_engine
from patients.dbmodels import models

from . import factories

REQUIRED_ARGS = ['name', 'surname', 'birthday', 'deceased']


@pytest.fixture(scope='module', autouse=True)
def db_create():
    db_engine.execute('drop schema if exists public cascade')
    db_engine.execute('create schema public')
    models.Base.metadata.create_all(db_engine)

    yield

    db_session.close_all()
    db_engine.execute('drop schema public cascade')


def test_default_values():
    patient = factories.Patient()

    assert patient.id is None
    assert patient.created is None
    assert patient.updated is None

    db_session.add(patient)
    db_session.commit()

    assert patient.id is not None
    assert patient.created is not None
    assert patient.updated is None

    patient.name = 'Jon'
    patient.surname = 'Snow'
    db_session.commit()

    assert patient.updated is not None


@pytest.mark.parametrize(
    'attr',
    REQUIRED_ARGS,
)
def test_required_values(attr):
    patient = factories.Patient()

    for arg in REQUIRED_ARGS:
        assert getattr(patient, arg, None) is not None

    setattr(patient, attr, None)
    db_session.add(patient)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
