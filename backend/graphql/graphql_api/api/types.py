from graphene_sqlalchemy import SQLAlchemyObjectType

from patients.dbmodels import models


class PatientType(SQLAlchemyObjectType):
    class Meta:
        model = models.Patient


class DiseaseType(SQLAlchemyObjectType):
    class Meta:
        model = models.Disease
