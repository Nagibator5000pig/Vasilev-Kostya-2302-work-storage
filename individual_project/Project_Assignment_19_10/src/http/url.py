from dataclasses import dataclass


class ParseError(Exception):
    pass


@dataclass
class Url:
    scheme: str
    host: str
    port: int
    path: str = "/"
    query: str = ""

    @classmethod
    def parse(cls, raw: str) -> "Url":
        if not raw or "://" not in raw:
            raise ParseError(f"Invalid URL: {raw}")

        scheme, rest = raw.split("://", 1)
        scheme = scheme.lower()
        if scheme not in ("http", "https"):
            raise ParseError(f"Unsupported scheme: {scheme}")

        if "?" in rest:
            rest, query = rest.split("?", 1)
        else:
            query = ""

        if "/" in rest:
            host_part, path_part = rest.split("/", 1)
            path = "/" + path_part
        else:
            host_part, path = rest, "/"

        if ":" in host_part:
            host, port_str = host_part.rsplit(":", 1)
            try:
                port = int(port_str)
            except ValueError as exc:
                raise ParseError(f"Invalid port: {port_str}") from exc
        else:
            host = host_part
            port = 443 if scheme == "https" else 80

        if not host:
            raise ParseError("Empty host")

        return cls(scheme=scheme, host=host, port=port, path=path or "/", query=query)
