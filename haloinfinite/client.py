from urllib.parse import urlencode

import requests

from haloinfinite.decorators import (
    spartan_token_required,
    user_token_required,
    xbox_user_token_required,
    xsts_halo_token_required,
)
from haloinfinite.exceptions import (
    BadRequestError,
    BandwidthLimitExceededError,
    ConflictError,
    ForbiddenError,
    GatewayTimeoutError,
    GoneError,
    InsufficientStorageError,
    InternalServerErrorError,
    LengthRequiredError,
    MethodNotAllowedError,
    NotAcceptableError,
    NotFoundError,
    NotImplementedAPIError,
    PreconditionFailedError,
    RequestedRangeNotSatisfiableError,
    RequestEntityTooLargeError,
    ServiceUnavailableError,
    TooManyRequestsError,
    UnauthorizedError,
    UnknownError,
    UnprocessableEntityError,
    UnsupportedMediaTypeError,
)
from haloinfinite.match import Match
from haloinfinite.response import Response
from haloinfinite.utils import DEFAULT_SCOPES, TokenType, validate_token_expiration


class HaloInfiniteAPIClient:
    AUTHORITY_URL = "https://login.live.com/"
    AUTH_ENDPOINT = "oauth20_authorize.srf"
    TOKEN_ENDPOINT = "oauth20_token.srf"

    XBOX_USER_URL = "https://user.auth.xboxlive.com/user/authenticate"
    XBOX_SECURITY_TOKEN_SERVICE_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"
    SPARTAN_TOKEN_URL = "https://settings.svc.halowaypoint.com/spartan-token"
    CLEARANCE_URL = "https://settings.svc.halowaypoint.com/oban/flight-configurations/titles/hi/audiences/RETAIL/players/xuid({})/active?sandbox=UNUSED&build=210921.22.01.10.1706-0"

    HALO_INFINITE_STATS_URL = "https://halostats.svc.halowaypoint.com/hi/"
    HALO_INFINITE_SKILL_URL = "https://skill.svc.halowaypoint.com/hi/"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_token: dict = None,
        xbox_user_token: dict = None,
        xsts_xbox_token: dict = None,
        xsts_halo_token: dict = None,
        spartan_token: dict = None,
        clearance_token: dict = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self._user_token = user_token
        self._xbox_user_token = xbox_user_token
        self._xsts_xbox_token = xsts_xbox_token
        self._xsts_halo_token = xsts_halo_token
        self._spartan_token = spartan_token
        self._clearance_token = clearance_token

        self.match = Match(self)

    @property
    def user_access_token(self) -> str:
        return self._user_token["access_token"]

    @property
    def xbox_user_token(self) -> str:
        validate_token_expiration(self._xbox_user_token, TokenType.XBOX_USER)
        return self._xbox_user_token["Token"]

    @property
    def xsts_xbox_token(self) -> str:
        validate_token_expiration(self._xsts_xbox_token, TokenType.XSTS_XBOX)
        return self._xsts_xbox_token["Token"]

    @property
    def xsts_halo_token(self) -> str:
        validate_token_expiration(self._xsts_halo_token, TokenType.XSTS_HALO)
        return self._xsts_halo_token["Token"]

    @property
    def spartan_token(self) -> str:
        validate_token_expiration(self._spartan_token, TokenType.SPARTAN)
        return self._spartan_token["SpartanToken"]

    @property
    def clearance_token(self) -> str:
        return self._clearance_token["FlightConfigurationId"]

    @property
    def xbox_user_id(self) -> str:
        return self._xsts_xbox_token["DisplayClaims"]["xui"][0]["xid"]

    def get_authorization_url(self, redirect_uri: str, scope: list = DEFAULT_SCOPES, state: str = None) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": " ".join(scope),
            "redirect_uri": redirect_uri,
        }
        if state:
            params["state"] = state
        return f"{self.AUTHORITY_URL}{self.AUTH_ENDPOINT}?{urlencode(params)}"

    def exchange_code(self, redirect_uri: str, code: str) -> Response:
        data = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        return self._post(f"{self.AUTHORITY_URL}{self.TOKEN_ENDPOINT}", data=data)

    def refresh_token(self, redirect_uri: str, refresh_token: str) -> Response:
        data = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        return self._post(f"{self.AUTHORITY_URL}{self.TOKEN_ENDPOINT}", data=data)

    def set_user_token(self, token: dict) -> None:
        self._user_token = token

    @user_token_required
    def get_xbox_user_token(self) -> Response:
        data = {
            "Properties": {
                "AuthMethod": "RPS",
                "RpsTicket": f"d={self.user_access_token}",
                "SiteName": "user.auth.xboxlive.com",
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }
        return self._post(self.XBOX_USER_URL, json=data)

    def set_xbox_user_token(self, token: dict) -> None:
        self._xbox_user_token = token

    @xbox_user_token_required
    def get_xsts_xbox_token(self) -> Response:
        return self.get_xsts_token("http://xboxlive.com")

    @xbox_user_token_required
    def get_xsts_halo_token(self) -> Response:
        return self.get_xsts_token("https://prod.xsts.halowaypoint.com/")

    @xbox_user_token_required
    def get_xsts_token(self, relying_party: str) -> Response:
        data = {
            "Properties": {"SandboxId": "RETAIL", "UserTokens": [self.xbox_user_token]},
            "RelyingParty": relying_party,
            "TokenType": "JWT",
        }
        return self._post(self.XBOX_SECURITY_TOKEN_SERVICE_URL, json=data)

    def set_xsts_xbox_token(self, token: dict) -> None:
        self._xsts_xbox_token = token

    def set_xsts_halo_token(self, token: dict) -> None:
        self._xsts_halo_token = token

    @xsts_halo_token_required
    def get_spartan_code(self) -> Response:
        data = {
            "Audience": "urn:343:s3:services",
            "MinVersion": "4",
            "Proof": [
                {
                    "Token": self.xsts_halo_token,
                    "TokenType": "Xbox_XSTSv3",
                }
            ],
        }
        return self._post(self.SPARTAN_TOKEN_URL, json=data)

    def set_spartan_token(self, token: dict) -> None:
        self._spartan_token = token

    @spartan_token_required
    def get_clearance_token(self) -> Response:
        headers = {"x-343-authorization-spartan": self.spartan_token}
        return self._get(self.CLEARANCE_URL.format(self.xbox_user_id), headers=headers)

    def set_clearance_token(self, token: dict) -> None:
        self._clearance_token = token

    def get_endpoints(self) -> Response:
        url = f"https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48"
        return self._client._get(url)

    def _get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request("PUT", url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request("PATCH", url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        _headers = {
            "Accept": "application/json",
        }
        if headers:
            _headers.update(headers)

        return self._parse(requests.request(method, url, headers=_headers, **kwargs))

    def _parse(self, response):
        status_code = response.status_code
        r = Response(original=response)
        if status_code in (200, 201, 202, 204, 206):
            return r
        elif status_code == 400:
            raise BadRequestError(r.data)
        elif status_code == 401:
            raise UnauthorizedError(r.data)
        elif status_code == 403:
            raise ForbiddenError(r.data)
        elif status_code == 404:
            raise NotFoundError(r.data)
        elif status_code == 405:
            raise MethodNotAllowedError(r.data)
        elif status_code == 406:
            raise NotAcceptableError(r.data)
        elif status_code == 409:
            raise ConflictError(r.data)
        elif status_code == 410:
            raise GoneError(r.data)
        elif status_code == 411:
            raise LengthRequiredError(r.data)
        elif status_code == 412:
            raise PreconditionFailedError(r.data)
        elif status_code == 413:
            raise RequestEntityTooLargeError(r.data)
        elif status_code == 415:
            raise UnsupportedMediaTypeError(r.data)
        elif status_code == 416:
            raise RequestedRangeNotSatisfiableError(r.data)
        elif status_code == 422:
            raise UnprocessableEntityError(r.data)
        elif status_code == 429:
            raise TooManyRequestsError(r.data)
        elif status_code == 500:
            raise InternalServerErrorError(r.data)
        elif status_code == 501:
            raise NotImplementedAPIError(r.data)
        elif status_code == 503:
            raise ServiceUnavailableError(r.data)
        elif status_code == 504:
            raise GatewayTimeoutError(r.data)
        elif status_code == 507:
            raise InsufficientStorageError(r.data)
        elif status_code == 509:
            raise BandwidthLimitExceededError(r.data)
        else:
            raise UnknownError(r.data)
