import socket
import threading
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


def test_i1_root(server):
    resp = HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/")
    assert resp.status == 200
    assert b"Hello" in resp.body


def test_i2_post_echo(server):
    resp = HttpClient(timeout=2.0).post(
        f"http://127.0.0.1:{server}/echo", body=b"abc", content_type="text/plain"
    )
    assert resp.status == 200
    assert resp.body == b"abc"
    assert resp.headers["Content-Type"] == "text/plain"


def test_i3_status_404(server):
    with pytest.raises(HttpError) as exc_info:
        HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/status/404")
    assert exc_info.value.status == 404


def test_i4_not_found(server):
    with pytest.raises(HttpError) as exc_info:
        HttpClient(timeout=2.0).get(f"http://127.0.0.1:{server}/nonexistent")
    assert exc_info.value.status == 404


def test_i5_100_sequential_gets(server):
    client = HttpClient(timeout=2.0)
    for _ in range(100):
        resp = client.get(f"http://127.0.0.1:{server}/")
        assert resp.status == 200


def test_i6_10_parallel_gets(server):
    client = HttpClient(timeout=2.0)
    errors = []

    def worker():
        try:
            r = client.get(f"http://127.0.0.1:{server}/")
            if r.status != 200:
                errors.append(r.status)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors


def test_i7_timeout(server):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.listen(1)

    def run():
        try:
            conn, _ = s.accept()
            time.sleep(1.0)
            conn.close()
        except OSError:
            pass
        finally:
            s.close()

    threading.Thread(target=run, daemon=True).start()
    client = HttpClient(timeout=0.1)
    with pytest.raises((socket.timeout, TimeoutError)):
        client.get(f"http://127.0.0.1:{port}/")


def test_i8_garbage_returns_400(server):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", server))
    s.sendall(b"GARBAGE\r\n\r\n")
    data = s.recv(4096)
    s.close()
    assert b"400" in data


def test_i9_keep_alive_3_requests(server):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", server))
    for _ in range(3):
        s.sendall(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
        data = s.recv(4096)
        assert b"200" in data
    s.close()


def test_i10_1000_requests_no_leaks(server):
    client = HttpClient(timeout=2.0)
    for _ in range(1000):
        resp = client.get(f"http://127.0.0.1:{server}/")
        assert resp.status == 200
