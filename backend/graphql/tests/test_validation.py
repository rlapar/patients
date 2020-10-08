from jsonschema.exceptions import ValidationError
import pytest


@pytest.mark.parametrize('offset', [0, 100, 10000])
def test_offset(validator, offset):
    assert validator.validate({'offset': offset}) is None


def test_offset_invalid(validator):
    with pytest.raises(ValidationError):
        validator.validate({'offset': -1})


@pytest.mark.parametrize('limit', [1, 100, 500])
def test_limit(validator, limit):
    assert validator.validate({'limit': limit}) is None


@pytest.mark.parametrize('limit', [-1, 0, 501])
def test_limit_invalid(validator, limit):
    with pytest.raises(ValidationError):
        validator.validate({'limit': limit})
