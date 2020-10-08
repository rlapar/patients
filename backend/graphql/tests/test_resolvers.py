import datetime as dt

from graphql_api.api.resolvers import (
    apply_basic_args,
    diseases,
    patients
)

CREATED_FROM = dt.datetime.utcnow() - dt.timedelta(days=5)
CREATED_TO = dt.datetime.utcnow() - dt.timedelta(days=2)
UPDATED_FROM = dt.datetime.utcnow() - dt.timedelta(days=4)
UPDATED_TO = dt.datetime.utcnow()

BASIC_ARGS = {
    'limit': 1,
    'offset': 0,
    'order': 'desc',
    'created_from': CREATED_FROM,
    'created_to': CREATED_TO,
    'updated_from': UPDATED_FROM,
    'updated_to': UPDATED_TO,
}

def test_apply_basic_args(mocker, model):
    mock_filtered_query = mocker.MagicMock()
    decorated_func = mocker.MagicMock(return_value=mock_filtered_query, __name__='resolve_patients')
    apply_basic_args(model)(decorated_func)(
        'some arg',
        some_kwarg='some_value',
        **BASIC_ARGS
    )

    decorated_func.assert_called_with('some arg', some_kwarg='some_value')
    mock_filtered_query.order_by.assert_called_with(model.created.desc())
    model.created.__ge__.assert_called_with(CREATED_FROM)
    model.created.__le__.assert_called_with(CREATED_TO)
    model.updated.__ge__.assert_called_with(UPDATED_FROM)
    model.updated.__le__.assert_called_with(UPDATED_TO)
    mock_filtered_query.order_by().limit.assert_called_with(1)
    mock_filtered_query.order_by().limit().offset.assert_called_with(0)


class TestPatientResolver:
    def test_resolve_patient(self, patch_type):
        mock_query = patch_type(patients, 'Patient').query
        patients.resolve_patient(None, None, patient_id=2)
        mock_query.get.assert_called_with(2)

    def test_resolve_patients(self, patch_type):
        mock_type = patch_type(patients, 'Patient')
        mock_type.birthday.__ge__.return_value = 'ge_birthday'
        mock_type.birthday.__le__.return_value = 'le_birthday'

        kwargs = {
            **BASIC_ARGS,
            'birthday_from': 'birthday_from',
            'birthday_to': 'birthday_to',
        }
        patients.resolve_patients(None, None, **kwargs)

        mock_type.birthday.__ge__.assert_called_with('birthday_from')
        mock_type.birthday.__le__.assert_called_with('birthday_to')


class TestDiseaseResolver:
    def test_resolve_disease(self, patch_type):
        mock_query = patch_type(diseases, 'Disease').query
        diseases.resolve_disease(None, None, disease_id=5)
        mock_query.get.assert_called_with(5)
