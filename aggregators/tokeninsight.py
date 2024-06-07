import requests
from typing import Any
from aggregators import Aggregator, PingResult, RequestMethod
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenInsightRating:
    tid: str
    rating_level: str
    rating_score: float
    underlying_technology_security_score: float
    token_performance_score: float
    ecosystem_development_score: float
    team_partners_investors_score: float
    token_economics_score: float
    roadmap_progress_score: float


class TokenInsightAggregator(Aggregator):
    def __init__(self, api_url: str, api_key: str) -> None:
        self._api_url = api_url
        self._api_key = api_key
        self._ping_endpoint = "/ping"

    def _send_request(self, endpoint: str, method: RequestMethod, headers: dict = None) -> Any:
        adapter = getattr(requests, method.value)
        prepared_url = f"{self._api_url}{endpoint}"
        return adapter(prepared_url, headers=headers)


    def _send_authenticated_request(self, endpoint: str, method: RequestMethod) -> Any:
        headers = { "TI_API_KEY": self._api_key }
        return self._send_request(endpoint, method, headers)

    def ping(self) -> PingResult:
        response = self._send_request(self._ping_endpoint, RequestMethod.GET)
        return PingResult.OK if response.status_code == 200 else PingResult.FAIL

    def _exclude_score(self, score: str) -> int:
        return float(score.strip("%"))

    def getRating(self, coin_id: str) -> TokenInsightRating:
        rating_endpoint = f"/rating/coin/{coin_id}"
        response = self._send_authenticated_request(rating_endpoint, RequestMethod.GET)
        serialized_response = response.json()

        data = serialized_response['data'][0]
        
        tid = data['tid']
        rating_level = data['rating_level']
        rating_score = float(data['rating_score'])
        underlying_technology_security_score = self._exclude_score(data['underlying_technology_security'])
        token_performance_score = self._exclude_score(data['token_performance'])
        ecosystem_development_score = self._exclude_score(data['ecosystem_development'])
        team_partners_investors_score = self._exclude_score(data['team_partners_investors'])
        token_economics_score = self._exclude_score(data['token_economics'])
        roadmap_progress_score = self._exclude_score(data['roadmap_progress'])

        return TokenInsightRating(
            tid,
            rating_level,
            rating_score,
            underlying_technology_security_score,
            token_performance_score,
            ecosystem_development_score,
            team_partners_investors_score,
            token_economics_score,
            roadmap_progress_score
        )