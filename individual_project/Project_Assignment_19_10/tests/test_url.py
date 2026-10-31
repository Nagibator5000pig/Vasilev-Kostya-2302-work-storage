import pytest
from src.http.url import Url, ParseError


def test_u1_parse_full_url():
    url = Url.parse("http://host:8080/path?q=1")
    assert url.scheme == "http"
    assert url.host == "host"
    assert url.port == 8080
    assert url.path == "/path"
    assert url.query == "q=1"


def test_u2_default_port_http():
    url = Url.parse("http://host/path")
    assert url.port == 80
    assert url.path == "/path"


def test_u3_garbage_raises():
    with pytest.raises(ParseError):
        Url.parse("garbage")


def test_https_default_port():
    url = Url.parse("https://example.com")
    assert url.port == 443
    assert url.path == "/"


def test_no_path():
    url = Url.parse("http://host")
    assert url.path == "/"
    assert url.query == ""


def test_query_only():
    url = Url.parse("http://host?q=1")
    assert url.path == "/"
    assert url.query == "q=1"


def test_bad_port():
    with pytest.raises(ParseError):
        Url.parse("http://host:abc/")


def test_empty_host():
    with pytest.raises(ParseError):
        Url.parse("http:///path")


def test_unsupported_scheme():
    with pytest.raises(ParseError):
        Url.parse("ftp://host/")
