import datetime

from copy import deepcopy

import pytest

# -- patient args --
NAME_VALID = "Jon"
NAME_INVALID = 42
SURNAME_VALID = "Snow"
SURNAME_INVALID = 42
BIRTHDAY_VALID = "2017-07-21T17:32:28Z"
BIRTHDAY_INVALID = "invalid"
DECEASED_VALID = True
DECEASED_INVALID = 5

PAYLOAD_VALID = {
    'name': NAME_VALID,
    'surname': SURNAME_VALID,
    'birthday': BIRTHDAY_VALID,
    'deceased': DECEASED_VALID
}

ENDPOINT_PREFIX = '/rest'
ENDPOINT = f'{ENDPOINT_PREFIX}/patients/create'


class TestBadRequest:
    @pytest.mark.parametrize('missing', [
        'name', 'surname', 'birthday'
    ])
    def test_required_args(self, client, missing):
        payload = deepcopy(PAYLOAD_VALID)
        payload.pop(missing)
        resp = client.post(ENDPOINT, json=payload, headers={'content-type': 'application/json'})
        assert resp.status_code == 400

    @pytest.mark.parametrize('arg, value', [
        ('name', NAME_INVALID),
        ('surname', SURNAME_INVALID),
        ('birthday', BIRTHDAY_INVALID),
        ('deceased', DECEASED_INVALID),
    ])
    def test_invalid_args(self, client, arg, value):
        payload = deepcopy(PAYLOAD_VALID)
        payload[arg] = value
        resp = client.post(ENDPOINT, json=payload, headers={'content-type': 'application/json'})
        assert resp.status_code == 400

    def test_invlid_birthday(self, client):
        payload = deepcopy(PAYLOAD_VALID)
        # time in future
        payload['birthday'] = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
        resp = client.post(ENDPOINT, json=payload, headers={'content-type': 'application/json'})
        assert resp.status_code == 400


class TestValidRequest:
    def test_valid_payload(self, mocker, client):
        mocker.patch('rest.api.patients.create.db_session')
        resp = client.post(ENDPOINT, json=PAYLOAD_VALID, headers={'content-type': 'application/json'})
        assert resp.status_code == 200
