from flask import g

from patients.dbmodels.models import Patient

from . import apply_basic_args


def resolve_patient(self, info, patient_id):
    g.logger.info("resolve.patient", patient_id=patient_id)
    return Patient.query.get(patient_id)


@apply_basic_args(Patient)
def resolve_patients(self, info, **kwargs):
    g.logger.info("resolve.patients", **kwargs)

    q = Patient.query

    if "birthday_from" in kwargs:
        q = q.filter(Patient.birthday >= kwargs.pop("birthday_from"))

    if "birthday_to" in kwargs:
        q = q.filter(Patient.birthday <= kwargs.pop("birthday_to"))

    q = q.filter_by(**kwargs)

    return q
