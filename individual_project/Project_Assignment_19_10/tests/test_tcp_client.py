import socket
import threading
import pytest

from src.net.tcp_client import TcpClient


@pytest.fixture
def fake_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 0))
    port = server.getsockname()[1]
    server.listen(1)

    def run():
        conn, _ = server.accept()
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nhi")
        conn.close()
        server.close()

    t = threading.Thread(target=run, daemon=True)
    t.start()
    yield port
    t.join(timeout=2)


def test_connect_and_recv(fake_server):
    client = TcpClient("127.0.0.1", fake_server, timeout=2.0)
    with client.connect() as sock:
        data = sock.recv(1024)
    assert data.startswith(b"HTTP/1.1 200")


def test_connect_refused():
    client = TcpClient("127.0.0.1", 1, timeout=0.5)
    with pytest.raises(ConnectionError):
        client.connect()
