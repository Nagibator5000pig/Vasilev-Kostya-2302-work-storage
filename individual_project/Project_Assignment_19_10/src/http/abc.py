from abc import ABC, abstractmethod

from src.http.request import Request
from src.http.response import Response


class AbstractParser(ABC):
    @abstractmethod
    def parse_request(self, raw: bytes) -> Request:
        ...

    @abstractmethod
    def parse_response(self, raw: bytes) -> Response:
        ...


class AbstractHandler(ABC):
    @abstractmethod
    def handle(self, req: Request) -> Response:
        ...
