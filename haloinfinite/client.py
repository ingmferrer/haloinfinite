import requests
from urllib.parse import urlencode
from haloinfinite.decorators import (
    spartan_token_required,
    user_token_required,
    xbox_user_token_required,
    xsts_halo_token_required,
)

from haloinfinite.utils import DEFAULT_SCOPES
from haloinfinite.match import Match


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

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self._user_token = None
        self._xbox_user_token = None
        self._xsts_xbox_token = None
        self._xsts_halo_token = None
        self._spartan_token = None
        self._clearance_id = None

        self.match = Match(self)

    @property
    def user_access_token(self):
        return self._user_token["access_token"]

    @property
    def xbox_user_token(self):
        return self._xbox_user_token["Token"]

    @property
    def xsts_xbox_token(self):
        return self._xsts_xbox_token["Token"]

    @property
    def xsts_halo_token(self):
        return self._xsts_halo_token["Token"]

    @property
    def spartan_token(self):
        return self._spartan_token["SpartanToken"]

    @property
    def clearance_id(self):
        return self._clearance_id["FlightConfigurationId"]

    @property
    def xbox_user_id(self):
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

    def exchange_code(self, redirect_uri: str, code: str):
        data = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        response = requests.post(f"{self.AUTHORITY_URL}{self.TOKEN_ENDPOINT}", data=data)
        return self._parse(response)

    def refresh_token(self, redirect_uri: str, refresh_token: str):
        data = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        response = requests.post(f"{self.AUTHORITY_URL}{self.TOKEN_ENDPOINT}", data=data)
        return self._parse(response)

    def set_user_token(self, token: dict) -> None:
        self._user_token = token

    @user_token_required
    def get_xbox_user_token(self):
        data = {
            "Properties": {
                "AuthMethod": "RPS",
                "RpsTicket": f"d={self.user_access_token}",
                "SiteName": "user.auth.xboxlive.com",
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }
        response = requests.post(self.XBOX_USER_URL, json=data)
        return self._parse(response)

    def set_xbox_user_token(self, token: dict) -> None:
        self._xbox_user_token = token

    @xbox_user_token_required
    def get_xsts_xbox_token(self):
        return self.get_xsts_token("http://xboxlive.com")

    @xbox_user_token_required
    def get_xsts_halo_token(self):
        return self.get_xsts_token("https://prod.xsts.halowaypoint.com/")

    @xbox_user_token_required
    def get_xsts_token(self, relying_party: str):
        data = {
            "Properties": {"SandboxId": "RETAIL", "UserTokens": [self.xbox_user_token]},
            "RelyingParty": relying_party,
            "TokenType": "JWT",
        }
        response = requests.post(self.XBOX_SECURITY_TOKEN_SERVICE_URL, json=data)
        return self._parse(response)

    def set_xsts_xbox_token(self, token: dict) -> None:
        self._xsts_xbox_token = token

    def set_xsts_halo_token(self, token: dict) -> None:
        self._xsts_halo_token = token

    @xsts_halo_token_required
    def get_spartan_code(self):
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
        response = requests.post(self.SPARTAN_TOKEN_URL, json=data, headers={"Accept": "application/json"})
        return self._parse(response)

    def set_spartan_token(self, token: dict) -> None:
        self._spartan_token = token

    @spartan_token_required
    def get_clearance_id(self):
        headers = {"x-343-authorization-spartan": self.spartan_token}
        response = requests.get(self.CLEARANCE_URL.format(self.xbox_user_id), headers=headers)
        return self._parse(response)

    def set_clearance_id(self, token: dict) -> None:
        self._clearance_id = token

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
        return response
