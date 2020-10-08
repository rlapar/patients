from flask import g

from patients.dbmodels.models import Disease

from ...errors import ValidationError
from ...schema import disease_schema
from ...utils import handle_exception


def handle_request(**kwargs):
    g.logger.info('diseases.get', payload=str(kwargs))
    try:
        disease = Disease.query.get(kwargs.get('disease_id'))
        if not disease:
            raise ValidationError(f"Disease with id={kwargs['disease_id']} not found in db.")
        return disease_schema.dump(disease).data
    except ValidationError as e:
        description = {'description': f'{e.__class__.__name__}: {str(e)}'}
        handle_exception(e, 'get_disease', 400, description)
