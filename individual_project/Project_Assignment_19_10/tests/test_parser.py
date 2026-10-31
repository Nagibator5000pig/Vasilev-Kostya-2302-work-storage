import pytest
from src.http.parser import Parser
from src.http.url import ParseError

parser = Parser()
parse_request = parser.parse_request
parse_response = parser.parse_response


def test_u4_parse_simple_request():
    req = parse_request(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    assert req.method == "GET"
    assert req.path == "/"
    assert req.headers["Host"] == "example.com"
    assert req.body == b""


def test_u5_parse_request_with_body():
    raw = (
        b"POST /echo HTTP/1.1\r\n"
        b"Host: localhost\r\n"
        b"Content-Length: 3\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"abc"
    )
    req = parse_request(raw)
    assert req.method == "POST"
    assert req.body == b"abc"
    assert req.headers["Content-Type"] == "text/plain"


def test_u6_no_host_raises():
    with pytest.raises(ParseError):
        parse_request(b"GET / HTTP/1.1\r\n\r\n")


def test_u9_chunked_response():
    raw = (
        b"HTTP/1.1 200 OK\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"\r\n"
        b"5\r\nHello\r\n"
        b"6\r\n World\r\n"
        b"0\r\n\r\n"
    )
    resp = parse_response(raw)
    assert resp.body == b"Hello World"


def test_u10_large_header_raises():
    huge_value = b"x" * (9 * 1024)
    raw = b"GET / HTTP/1.1\r\nHost: a\r\nX-Big: " + huge_value + b"\r\n\r\n"
    with pytest.raises(ParseError):
        parse_request(raw)


def test_response_basic():
    raw = b"HTTP/1.1 404 Not Found\r\nContent-Length: 3\r\n\r\n404"
    resp = parse_response(raw)
    assert resp.status == 404
    assert resp.reason == "Not Found"
    assert resp.body == b"404"


def test_request_without_separator_raises():
    with pytest.raises(ParseError):
        parse_request(b"GET / HTTP/1.1")


def test_bad_header_line_raises():
    with pytest.raises(ParseError):
        parse_request(b"GET / HTTP/1.1\r\nBadHeader\r\n\r\n")


def test_body_truncated_by_content_length():
    raw = (
        b"POST /x HTTP/1.1\r\n"
        b"Host: a\r\n"
        b"Content-Length: 2\r\n"
        b"\r\n"
        b"abcdef"
    )
    req = parse_request(raw)
    assert req.body == b"ab"
