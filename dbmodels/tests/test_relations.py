import pytest


from patients.dbmodels.database import db_session, db_engine
from patients.dbmodels import models

from . import factories


@pytest.fixture(scope='module', autouse=True)
def db_create():
    db_engine.execute('drop schema if exists public cascade')
    db_engine.execute('create schema public')
    models.Base.metadata.create_all(db_engine)

    yield

    db_session.close_all()
    db_engine.execute('drop schema public cascade')


def test_patients_diseases_1_to_n():
    disease1 = factories.Disease()
    disease2 = factories.Disease()
    disease3 = factories.Disease()

    patient = factories.Patient(diseases=[disease1, disease2, disease3])

    db_session.add(patient)
    db_session.commit()

    assert disease1.patients == [patient]
    assert disease2.patients == [patient]
    assert disease3.patients == [patient]

    db_session.rollback()


def test_patients_diseases_n_to_1():
    patient1 = factories.Patient()
    patient2 = factories.Patient()

    disease = factories.Disease(patients=[patient1, patient2])

    db_session.add(disease)
    db_session.commit()

    assert patient1.diseases == [disease]
    assert patient2.diseases == [disease]

    db_session.rollback()


def test_patients_diseases_m_to_n():
    patient1 = factories.Patient()
    patient2 = factories.Patient()
    patient3 = factories.Patient()

    disease1 = factories.Disease(patients=[patient1, patient2])
    disease2 = factories.Disease(patients=[patient2, patient3])
    disease3 = factories.Disease(patients=[patient1, patient3])

    db_session.add_all([disease1, disease2, disease3])
    db_session.commit()

    assert patient1.diseases == [disease1, disease3]
    assert patient2.diseases == [disease1, disease2]
    assert patient3.diseases == [disease2, disease3]

    db_session.rollback()
