from src.http.errors import HttpError

from src.http.request import Request
from src.http.serializer import serialize_request
from src.http.url import Url
from src.net.tcp_client import TcpClient
from src.http.parser import Parser


class HttpClient:
    def __init__(self, timeout: float = 5.0):
        self._timeout = timeout
        self._parser = Parser()
        self._max_redirects = 0

    def follow_redirects(self, max_redirects: int = 5):
        self._max_redirects = max_redirects

    def set_timeout(self, ms: int):
        self._timeout = ms / 1000.0

    def get(self, url: str, headers: dict | None = None):
        return self._request("GET", url, headers=headers)

    def post(self, url: str, body: bytes, content_type: str = "application/octet-stream",
             headers: dict | None = None):
        h = dict(headers or {})
        h.setdefault("Content-Type", content_type)
        h.setdefault("Content-Length", str(len(body)))
        return self._request("POST", url, headers=h, body=body)

    def _request(self, method: str, url_str: str, headers: dict | None = None, body: bytes = b""):
        url = Url.parse(url_str)
        h = dict(headers or {})
        h.setdefault("Host", url.host if url.port in (80, 443) else f"{url.host}:{url.port}")

        path = url.path + (f"?{url.query}" if url.query else "")
        req = Request(method=method, path=path, headers=h, body=body)

        redirects = 0
        while True:
            client = TcpClient(url.host, url.port, self._timeout, use_ssl=(url.scheme == "https"))
            with client.connect() as sock:
                sock.send_all(serialize_request(req))
                raw = _read_response(sock)
            resp = self._parser.parse_response(raw)

            if resp.status in (301, 302, 303, 307) and "Location" in resp.headers:
                if redirects >= self._max_redirects:
                    break
                redirects += 1
                url = Url.parse(resp.headers["Location"])
                h["Host"] = url.host if url.port in (80, 443) else f"{url.host}:{url.port}"
                path = url.path + (f"?{url.query}" if url.query else "")
                req = Request(method=method, path=path, headers=h, body=body)
                continue
            break

        if 400 <= resp.status < 600:
            raise HttpError(resp.status, resp.reason)
        return resp


def _read_response(sock) -> bytes:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("Connection closed before headers")
        data += chunk

    head, _, rest = data.partition(b"\r\n\r\n")
    headers_lower = head.lower()

    if b"transfer-encoding: chunked" in headers_lower:
        while b"\r\n0\r\n\r\n" not in rest and not rest.endswith(b"0\r\n\r\n"):
            chunk = sock.recv(4096)
            if not chunk:
                break
            rest += chunk
    elif b"content-length:" in headers_lower:
        length = _extract_content_length(head)
        if length is not None:
            while len(rest) < length:
                chunk = sock.recv(4096)
                if not chunk:
                    raise ConnectionError("Connection closed before body")
                rest += chunk
    else:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            rest += chunk

    return head + b"\r\n\r\n" + rest


def _extract_content_length(head: bytes) -> int | None:
    for line in head.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            try:
                return int(line.split(b":", 1)[1].strip())
            except ValueError:
                return None
    return None
