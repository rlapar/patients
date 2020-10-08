import pytest

from sqlalchemy.exc import IntegrityError

from patients.dbmodels.database import db_session, db_engine
from patients.dbmodels import models

from . import factories

REQUIRED_ARGS = ['name', 'international_code']


@pytest.fixture(scope='module', autouse=True)
def db_create():
    db_engine.execute('drop schema if exists public cascade')
    db_engine.execute('create schema public')
    models.Base.metadata.create_all(db_engine)

    yield

    db_session.close_all()
    db_engine.execute('drop schema public cascade')


def test_default_values():
    disease = factories.Disease()

    assert disease.id is None
    assert disease.created is None
    assert disease.updated is None

    db_session.add(disease)
    db_session.commit()

    assert disease.id is not None
    assert disease.created is not None
    assert disease.updated is None

    disease.name = 'Cancer'
    db_session.commit()

    assert disease.updated is not None


@pytest.mark.parametrize(
    'attr',
    REQUIRED_ARGS,
)
def test_required_values(attr):
    disease = factories.Disease()

    for arg in REQUIRED_ARGS:
        assert getattr(disease, arg, None) is not None

    setattr(disease, attr, None)
    db_session.add(disease)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
