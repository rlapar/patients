from flask import g

from patients.dbmodels.models import Disease

from . import apply_basic_args


def resolve_disease(self, info, disease_id):
    g.logger.info("resolve.disease", disease_id=disease_id)
    return Disease.query.get(disease_id)


@apply_basic_args(Disease)
def resolve_diseases(self, info, **kwargs):
    g.logger.info("resolve.diseases", **kwargs)
    return Disease.query.filter_by(**kwargs)
