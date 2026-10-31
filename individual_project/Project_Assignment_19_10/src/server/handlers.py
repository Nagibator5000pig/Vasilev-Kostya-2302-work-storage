import json
from datetime import datetime, timezone

from src.http.abc import AbstractHandler
from src.http.request import Request
from src.http.response import Response


class RootHandler(AbstractHandler):
    def handle(self, req: Request) -> Response:
        body = b"<html><body><h1>Hello</h1></body></html>"
        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": "text/html; charset=utf-8"},
            body=body,
        )


class EchoHandler(AbstractHandler):
    def handle(self, req: Request) -> Response:
        content_type = req.headers.get("Content-Type", "application/octet-stream")
        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": content_type},
            body=req.body,
        )


class TimeHandler(AbstractHandler):
    def handle(self, req: Request) -> Response:
        now = datetime.now(timezone.utc).isoformat()
        body = json.dumps({"time": now}).encode("utf-8")
        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": "application/json"},
            body=body,
        )


class HeadersHandler(AbstractHandler):
    def handle(self, req: Request) -> Response:
        body = json.dumps(req.headers).encode("utf-8")
        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": "application/json"},
            body=body,
        )
