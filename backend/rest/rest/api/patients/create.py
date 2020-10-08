import datetime
import pytz

from flask import g

from patients.dbmodels.models import Patient
from patients.dbmodels.database import db_session

from ...errors import ValidationError
from ...schema import patient_schema
from ...utils import handle_exception, parse_rfc3339_datetime

def validate_kwargs(**kwargs):
    patient_args = kwargs.get('body')
    birthday = parse_rfc3339_datetime(patient_args['birthday'])
    if birthday > datetime.datetime.utcnow().replace(tzinfo=pytz.UTC):
        raise ValidationError("Birthday in future")
    patient_args['birthday'] = birthday

    return patient_args

def handle_request(**kwargs):
    g.logger.info('patients.create', payload=str(kwargs))
    try:
        patient_args = validate_kwargs(**kwargs)
        patient = Patient(**patient_args)
        db_session.add(patient)
        db_session.commit()
        return patient_schema.dump(patient).data
    except ValidationError as e:
        db_session.rollback()
        description = {'description': f'{e.__class__.__name__}: {str(e)}'}
        handle_exception(e, 'create_patient', 400, description)
