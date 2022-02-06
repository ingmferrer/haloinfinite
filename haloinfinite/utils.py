from datetime import datetime
from enum import Enum
from dateutil.parser import parse as date_parse

from haloinfinite.exceptions import TokenExpiredError


DEFAULT_SCOPES = ["Xboxlive.signin", "Xboxlive.offline_access"]


class TokenType(Enum):
    USER = 0
    XBOX_USER = 1
    XSTS_XBOX = 2
    XSTS_HALO = 3
    SPARTAN = 4
    CLEARANCE = 5


def validate_token_expiration(token: dict, type: TokenType):
    expiration = token["ExpiresUtc"]["ISO8601Date"] if type == TokenType.SPARTAN else token["NotAfter"]
    if date_parse(expiration).timestamp() < datetime.now().timestamp():
        raise TokenExpiredError(f"Your {type.name} token has expired.")
