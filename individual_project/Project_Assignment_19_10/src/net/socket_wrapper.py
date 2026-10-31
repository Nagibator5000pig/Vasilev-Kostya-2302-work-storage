import socket
from typing import Optional


class Socket:
    def __init__(self, sock: socket.socket):
        self._sock: Optional[socket.socket] = sock

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        try:
            if self._sock is not None:
                self._sock.close()
        finally:
            self._sock = None

    def send_all(self, data: bytes):
        if self._sock is None:
            raise RuntimeError("Socket is closed")
        self._sock.sendall(data)

    def recv(self, n: int) -> bytes:
        if self._sock is None:
            raise RuntimeError("Socket is closed")
        return self._sock.recv(n)

    def settimeout(self, seconds: float):
        if self._sock is None:
            raise RuntimeError("Socket is closed")
        self._sock.settimeout(seconds)
