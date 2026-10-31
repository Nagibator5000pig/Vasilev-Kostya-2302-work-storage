import socket


class TcpServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self._host = host
        self._port = port
        self._socket: socket.socket | None = None

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self._host, self._port))
        s.listen(5)
        self._socket = s

    def accept(self) -> tuple[socket.socket, tuple]:
        if self._socket is None:
            raise RuntimeError("Server not started")
        return self._socket.accept()

    def close(self):
        if self._socket is not None:
            try:
                self._socket.close()
            finally:
                self._socket = None
