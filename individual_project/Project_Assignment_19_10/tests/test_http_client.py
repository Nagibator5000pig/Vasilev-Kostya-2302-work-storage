import socket
import threading
import pytest

from src.client.http_client import HttpClient
from src.http.errors import HttpError


@pytest.fixture
def fake_http_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    port = server.getsockname()[1]
    server.listen(5)

    def handle():
        while True:
            try:
                conn, _ = server.accept()
            except OSError:
                break
            try:
                req = conn.recv(4096)
                path = req.split(b" ")[1] if b" " in req else b"/"
                if path == b"/echo":
                    body = req.split(b"\r\n\r\n", 1)[1] if b"\r\n\r\n" in req else b""
                    resp = (
                        b"HTTP/1.1 200 OK\r\n"
                        b"Content-Type: text/plain\r\n"
                        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                        b"\r\n" + body
                    )
                elif path == b"/404":
                    resp = b"HTTP/1.1 404 Not Found\r\nContent-Length: 3\r\n\r\n404"
                else:
                    resp = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
                conn.sendall(resp)
            finally:
                conn.close()

    t = threading.Thread(target=handle, daemon=True)
    t.start()
    yield port
    server.close()
    t.join(timeout=2)


def test_get_hello(fake_http_server):
    client = HttpClient(timeout=2.0)
    resp = client.get(f"http://127.0.0.1:{fake_http_server}/")
    assert resp.status == 200
    assert resp.body == b"Hello"


def test_get_404(fake_http_server):
    client = HttpClient(timeout=2.0)
    with pytest.raises(HttpError) as exc_info:
        client.get(f"http://127.0.0.1:{fake_http_server}/404")
    assert exc_info.value.status == 404


def test_post_echo(fake_http_server):
    client = HttpClient(timeout=2.0)
    resp = client.post(
        f"http://127.0.0.1:{fake_http_server}/echo",
        body=b"abc",
        content_type="text/plain",
    )
    assert resp.status == 200
    assert resp.body == b"abc"
    assert resp.headers["Content-Type"] == "text/plain"


def test_timeout():
    import socket
    import threading
    import time
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
    with pytest.raises(socket.timeout):
        client.get(f"http://127.0.0.1:{port}/")
