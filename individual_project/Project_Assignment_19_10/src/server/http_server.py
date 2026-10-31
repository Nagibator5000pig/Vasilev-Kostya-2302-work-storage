import socket
import threading
import traceback

from src.log_config import setup_logging
from src.http.response import Response
from src.http.serializer import serialize_response
from src.http.url import ParseError
from src.net.tcp_server import TcpServer
from src.server.router import Router
from src.http.parser import Parser


class HttpServer:
    def __init__(self, router: Router, host: str = "0.0.0.0", port: int = 8080):
        self._router = router
        self._host = host
        self._port = port
        self._tcp = TcpServer(host, port)
        self._thread: threading.Thread | None = None
        self._running = threading.Event()
        self._parser = Parser()
        self._logger = setup_logging()
        self.on_request = None

    def start(self):
        if self._running.is_set():
            return
        self._tcp.start()
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._logger.info("Server started on %s:%d", self._host, self._port)
        self._thread.start()

    def stop(self):
        self._logger.info("Server stopping")
        self._running.clear()
        self._tcp.close()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

    def is_running(self) -> bool:
        return self._running.is_set()

    def _loop(self):
        while self._running.is_set():
            try:
                conn, addr = self._tcp.accept()
            except OSError:
                break
            try:
                self._handle_connection(conn, addr)
            except Exception:
                traceback.print_exc()
            finally:
                try:
                    conn.close()
                except OSError:
                    pass

    def _handle_connection(self, conn: socket.socket, addr):
        conn.settimeout(5.0)
        try:
            while True:
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(4096)
                    if not chunk:
                        return
                    data += chunk

                head, _, rest = data.partition(b"\r\n\r\n")
                length = _content_length(head)
                if length is not None:
                    while len(rest) < length:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        rest += chunk
                full = head + b"\r\n\r\n" + rest

                try:
                    req = self._parser.parse_request(full)
                    resp = self._router.dispatch(req)
                except ParseError as e:
                    resp = Response(status=400, reason="Bad Request", body=str(e).encode("utf-8"))
                except Exception:
                    resp = Response(status=500, reason="Internal Server Error", body=b"500")

                if 'req' in locals():
                    self._logger.info("%s %s -> %d", req.method, req.path, resp.status)
                else:
                    self._logger.warning("Bad request -> %d", resp.status)

                if self.on_request:
                    self.on_request(req if 'req' in locals() else None, resp)

                conn.sendall(serialize_response(resp))

                if 'req' not in locals():
                    return
                connection_header = req.headers.get("Connection", "").lower()
                if connection_header == "close":
                    return
        except (socket.timeout, TimeoutError, ConnectionResetError):
            pass


def _content_length(head: bytes) -> int | None:
    for line in head.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            try:
                return int(line.split(b":", 1)[1].strip())
            except ValueError:
                return None
    return None
