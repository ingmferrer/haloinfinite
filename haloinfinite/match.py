from haloinfinite.decorators import spartan_token_required, xsts_xbox_token_required
from haloinfinite.response import Response


class Match(object):
    def __init__(self, client) -> None:
        self._client = client

    @spartan_token_required
    def get_match_privacy(self) -> Response:
        headers = {"x-343-authorization-spartan": self._client.spartan_token}
        url = f"{self._client.HALO_INFINITE_STATS_URL}players/xuid({self._client.xbox_user_id})/matches-privacy"
        return self._client._get(url, headers=headers)

    @spartan_token_required
    def get_match_count(self) -> Response:
        headers = {"x-343-authorization-spartan": self._client.spartan_token}
        url = f"{self._client.HALO_INFINITE_STATS_URL}players/xuid({self._client.xbox_user_id})/matches/count"
        return self._client._get(url, headers=headers)

    @spartan_token_required
    def get_match_history(self) -> Response:
        headers = {"x-343-authorization-spartan": self._client.spartan_token}
        url = f"{self._client.HALO_INFINITE_STATS_URL}players/xuid({self._client.xbox_user_id})/matches"
        return self._client._get(url, headers=headers)

    @spartan_token_required
    def get_match_stats(self, match_id: str) -> Response:
        headers = {"x-343-authorization-spartan": self._client.spartan_token}
        url = f"{self._client.HALO_INFINITE_STATS_URL}matches/{match_id}/stats"
        return self._client._get(url, headers=headers)

    @spartan_token_required
    def get_match_skill(self, match_id: str, player_id: str) -> Response:
        headers = {"x-343-authorization-spartan": self._client.spartan_token}
        url = f"{self._client.HALO_INFINITE_SKILL_URL}matches/{match_id}/skill?players=xuid({player_id})"
        return self._client._get(url, headers=headers)

    @xsts_xbox_token_required
    @spartan_token_required
    def get_match_progression(self, match_id: str) -> Response:
        headers = {"x-343-authorization-spartan": self._client.spartan_token}
        url = f"{self._client.HALO_INFINITE_STATS_URL}players/xuid({self._client.xbox_user_id})/matches/{match_id}/progression"
        return self._client._get(url, headers=headers)
