from typing import Callable

from src.http.request import Request
from src.http.response import Response

Handler = Callable[[Request], Response]


class Router:
    def __init__(self):
        self._routes: dict[tuple[str, str], Handler] = {}

    def route(self, method: str, path: str, handler: Handler):
        self._routes[(method.upper(), path)] = handler

    def dispatch(self, req: Request) -> Response:
        key = (req.method.upper(), req.path)
        if key in self._routes:
            return self._routes[key](req)

        if req.path.startswith("/status/"):
            try:
                code = int(req.path.split("/")[-1])
                return Response(status=code, body=b"")
            except ValueError:
                return Response(status=400, reason="Bad Request", body=b"Bad code")

        return Response(status=404, reason="Not Found", body=b"404 Not Found")
