import socket
import ssl

from src.net.socket_wrapper import Socket


class TcpClient:

    def __init__(self, host: str, port: int, timeout: float = 5.0, use_ssl: bool = False):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._use_ssl = use_ssl

    def connect(self) -> Socket:
        raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw.settimeout(self._timeout)
        try:
            raw.connect((self._host, self._port))
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            raw.close()
            raise ConnectionError(f"Failed to connect to {self._host}:{self._port}: {e}") from e
        if self._use_ssl:
            ctx = ssl.create_default_context()
            raw = ctx.wrap_socket(raw, server_hostname=self._host)
        return Socket(raw)
