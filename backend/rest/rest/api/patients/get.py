from flask import g

from patients.dbmodels.models import Patient

from ...errors import ValidationError
from ...schema import patient_schema
from ...utils import handle_exception


def handle_request(**kwargs):
    g.logger.info('patients.get', payload=str(kwargs))
    try:
        patient = Patient.query.get(kwargs.get('patient_id'))
        if not patient:
            raise ValidationError(f"Patient with id={kwargs['patient_id']} not found in db.")
        return patient_schema.dump(patient).data
    except ValidationError as e:
        description = {'description': f'{e.__class__.__name__}: {str(e)}'}
        handle_exception(e, 'get_patient', 400, description)
