import iso8601
import structlog
from connexion import ProblemException
from connexion.json_schema import Draft4RequestValidator

from .errors import ValidationError

log = structlog.get_logger()
ERROR_MAP = {503: 'DB Error',
             404: 'Not Found',
             400: 'Bad request'}

validator_map = {'body': Draft4RequestValidator}


def handle_exception(error, where, code, description, additional=None):
    if additional:
        log.exception(where, description=description, **additional)
    else:
        log.exception(where, description=description)
    raise ProblemException(code, ERROR_MAP[code], description)


def parse_rfc3339_datetime(date_str):
    try:
        return iso8601.parse_date(date_str)
    except iso8601.ParseError as e:
        raise ValidationError(f"Invalid date string {date_str}.")
