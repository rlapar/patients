import graphene

from .types import (
    DiseaseType,
    PatientType
)
from .resolvers.diseases import resolve_disease, resolve_diseases
from .resolvers.patients import resolve_patient, resolve_patients


basic_args = dict(
    limit=graphene.Int(default_value=10, description="Limit between 0 and 500"),
    offset=graphene.Int(default_value=0, description="Offset"),
    order=graphene.String(default_value='desc', description="Ordering"),
    created=graphene.String(),
    updated=graphene.String(),
    created_from=graphene.DateTime(),
    created_to=graphene.DateTime(),
    updated_from=graphene.DateTime(),
    updated_to=graphene.DateTime(),
)

patient_args = dict(
    **basic_args,
    name=graphene.String(),
    surname=graphene.String(),
    birthday=graphene.String(),
    birthday_from=graphene.String(),
    birthday_to=graphene.String(),
)

disease_args = dict(
    **basic_args,
    name=graphene.String(),
    international_code=graphene.String(),
)


class Query(graphene.ObjectType):
    disease = graphene.Field(DiseaseType, disease_id=graphene.ID(name="id"), resolver=resolve_disease)
    diseases = graphene.List(DiseaseType, **disease_args, resolver=resolve_diseases)

    patient = graphene.Field(PatientType, patient_id=graphene.ID(name="id"), resolver=resolve_patient)
    patients = graphene.List(PatientType, **patient_args, resolver=resolve_patients)
