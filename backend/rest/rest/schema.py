from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from patients.dbmodels import models


class DiseaseSchema(ModelSchema):
    class Meta:
        model = models.Disease


class PatientSchema(ModelSchema):
    diseases = fields.Nested(DiseaseSchema, many=True, exclude=["patients"])

    class Meta:
        model = models.Patient


disease_schema = DiseaseSchema(exclude=["patients"])
patient_schema = PatientSchema()
