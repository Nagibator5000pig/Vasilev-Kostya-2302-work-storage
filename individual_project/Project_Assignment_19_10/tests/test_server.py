import socket
import time
import pytest

from src.client.http_client import HttpClient
from src.server.handlers import RootHandler, EchoHandler, TimeHandler, HeadersHandler
from src.server.http_server import HttpServer
from src.server.router import Router
from src.http.errors import HttpError


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture
def server():
    router = Router()
    router.route("GET", "/", RootHandler().handle)
    router.route("POST", "/echo", EchoHandler().handle)
    router.route("GET", "/time", TimeHandler().handle)
    router.route("GET", "/headers", HeadersHandler().handle)

    port = _free_port()
    srv = HttpServer(router, host="127.0.0.1", port=port)
    srv.start()
    time.sleep(0.1)
    yield port
    srv.stop()


def test_root(server):
    resp = HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/")
    assert resp.status == 200
    assert b"Hello" in resp.body


def test_echo(server):
    resp = HttpClient(timeout=2.0).post(
        f"http://127.0.0.1:{server}/echo", body=b"abc", content_type="text/plain"
    )
    assert resp.status == 200
    assert resp.body == b"abc"
    assert resp.headers["Content-Type"] == "text/plain"


def test_time_json(server):
    resp = HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/time")
    assert resp.status == 200
    assert b"time" in resp.body


def test_status_code(server):
    with pytest.raises(HttpError) as exc_info:
        HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/status/418")
    assert exc_info.value.status == 418


def test_404(server):
    with pytest.raises(HttpError) as exc_info:
        HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/nonexistent")
    assert exc_info.value.status == 404


def test_bad_request(server):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", server))
    s.sendall(b"GARBAGE\r\n\r\n")
    data = s.recv(4096)
    s.close()
    assert b"400" in data


def test_server_stop_frees_port(server):
    HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/")
