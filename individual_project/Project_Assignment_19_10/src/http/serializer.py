from datetime import datetime, timezone
from src.http.request import Request
from src.http.response import Response


def serialize_request(req: Request) -> bytes:
    lines = [f"{req.method} {req.path} {req.version}"]
    for name, value in req.headers.items():
        lines.append(f"{name}: {value}")
    head = "\r\n".join(lines) + "\r\n\r\n"
    return head.encode("utf-8") + req.body


def serialize_response(resp: Response) -> bytes:
    headers = dict(resp.headers)
    if "Content-Length" not in headers and "Transfer-Encoding" not in headers:
        headers["Content-Length"] = str(len(resp.body))
    if "Date" not in headers:
        headers["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    reason = resp.reason or _reason_phrase(resp.status)
    lines = [f"{resp.version} {resp.status} {reason}"]
    for name, value in headers.items():
        lines.append(f"{name}: {value}")
    head = "\r\n".join(lines) + "\r\n\r\n"
    return head.encode("utf-8") + resp.body


_REASONS = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    418: "I'm a teapot",
    500: "Internal Server Error",
}


def _reason_phrase(status: int) -> str:
    return _REASONS.get(status, "")
