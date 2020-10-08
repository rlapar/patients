from flask import g

from patients.dbmodels.models import Disease
from patients.dbmodels.database import db_session

from ...errors import ValidationError
from ...schema import disease_schema
from ...utils import handle_exception

def validate_kwargs(**kwargs):
    print(kwargs)
    disease_args = kwargs.get('body')
    existing_names_diseases = db_session.query(Disease).filter(Disease.name == disease_args['name']).all()
    if existing_names_diseases:
        raise ValidationError(f'Disease with name {disease_args["name"]} already exists in DB.')
    existing_codes_diseases = db_session.query(Disease).filter(Disease.international_code == disease_args['international_code']).all()
    if existing_codes_diseases:
        raise ValidationError(f'Disease with code {disease_args["international_code"]} already exists in DB.')

    return disease_args

def handle_request(**kwargs):
    g.logger.info('diseases.create', payload=str(kwargs))
    try:
        disease_args = validate_kwargs(**kwargs)
        disease = Disease(**disease_args)
        db_session.add(disease)
        db_session.commit()
        return disease_schema.dump(disease).data
    except ValidationError as e:
        db_session.rollback()
        description = {'description': f'{e.__class__.__name__}: {str(e)}'}
        handle_exception(e, 'create_disease', 400, description)
