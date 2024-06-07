from typing import Any
from abc import ABC, abstractmethod
from enum import Enum


class PingResult(Enum):
    OK = "OK"
    FAIL = "FAIL"


class RequestMethod(Enum):
    GET = "get"
    POST = "post"


class Aggregator(ABC):
    @abstractmethod
    def __init__(self, url: str, api_key: str) -> None:
        pass

    @abstractmethod
    def ping(self) -> PingResult:
        pass

    @abstractmethod
    def _send_request(self, endpoint: str, method: RequestMethod, headers: dict = None) -> Any:
        pass  

    @abstractmethod
    def _send_authenticated_request(self, endpoint: str, method: RequestMethod) -> Any:
        pass