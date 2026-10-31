from src.http.request import Request
from src.http.response import Response
from src.http.url import ParseError
from src.http.abc import AbstractParser

MAX_HEADER_SIZE = 8 * 1024


def _split_head_body(raw: bytes) -> tuple[bytes, bytes]:
    idx = raw.find(b"\r\n\r\n")
    if idx == -1:
        raise ParseError("No header/body separator")
    head = raw[:idx]
    body = raw[idx + 4:]
    return head, body


def _parse_headers(lines: list[bytes]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in lines:
        if not line:
            continue
        if b":" not in line:
            raise ParseError(f"Invalid header line: {line!r}")
        name, value = line.split(b":", 1)
        headers[name.decode("latin-1").strip()] = value.decode("latin-1").strip()
    return headers


def _decode_chunked(data: bytes) -> bytes:
    result = b""
    i = 0
    while i < len(data):
        line_end = data.find(b"\r\n", i)
        if line_end == -1:
            raise ParseError("Invalid chunked encoding")
        size_line = data[i:line_end].split(b";", 1)[0]
        try:
            size = int(size_line, 16)
        except ValueError as exc:
            raise ParseError(f"Invalid chunk size: {size_line!r}") from exc
        i = line_end + 2
        if size == 0:
            break
        result += data[i:i + size]
        i += size + 2
    return result


class Parser(AbstractParser):
    def parse_request(self, raw: bytes) -> Request:
        head, body = _split_head_body(raw)
        if len(head) > MAX_HEADER_SIZE:
            raise ParseError("Headers too large")

        lines = head.split(b"\r\n")
        if not lines:
            raise ParseError("Empty request")

        start = lines[0].decode("latin-1")
        parts = start.split(" ")
        if len(parts) != 3:
            raise ParseError(f"Invalid request line: {start!r}")
        method, path, version = parts
        if not version.startswith("HTTP/"):
            raise ParseError(f"Invalid version: {version}")

        headers = _parse_headers(lines[1:])
        if "Host" not in headers:
            raise ParseError("Missing Host header")

        if "Content-Length" in headers:
            length = int(headers["Content-Length"])
            body = body[:length]
        elif headers.get("Transfer-Encoding", "").lower() == "chunked":
            body = _decode_chunked(body)

        return Request(method=method.upper(), path=path, version=version, headers=headers, body=body)

    def parse_response(self, raw: bytes) -> Response:
        head, body = _split_head_body(raw)
        if len(head) > MAX_HEADER_SIZE:
            raise ParseError("Headers too large")

        lines = head.split(b"\r\n")
        if not lines:
            raise ParseError("Empty response")

        start = lines[0].decode("latin-1")
        parts = start.split(" ", 2)
        if len(parts) < 2:
            raise ParseError(f"Invalid status line: {start!r}")
        version = parts[0]
        status = int(parts[1])
        reason = parts[2] if len(parts) > 2 else ""
        if not version.startswith("HTTP/"):
            raise ParseError(f"Invalid version: {version}")

        headers = _parse_headers(lines[1:])

        if "Content-Length" in headers:
            length = int(headers["Content-Length"])
            body = body[:length]
        elif headers.get("Transfer-Encoding", "").lower() == "chunked":
            body = _decode_chunked(body)

        return Response(status=status, reason=reason, version=version, headers=headers, body=body)
