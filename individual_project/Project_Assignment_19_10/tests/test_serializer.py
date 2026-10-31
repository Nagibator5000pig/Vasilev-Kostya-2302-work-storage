from src.http.request import Request
from src.http.response import Response
from src.http.serializer import serialize_request, serialize_response


def test_u7_request_ends_with_double_crlf():
    req = Request(method="GET", path="/")
    data = serialize_request(req)
    assert b"\r\n\r\n" in data
    assert data.startswith(b"GET / HTTP/1.1\r\n")


def test_u7b_request_with_headers_and_body():
    req = Request(
        method="POST",
        path="/echo",
        headers={"Content-Type": "text/plain", "Content-Length": "3"},
        body=b"abc",
    )
    data = serialize_request(req)
    assert b"POST /echo HTTP/1.1\r\n" in data
    assert b"Content-Type: text/plain\r\n" in data
    assert data.endswith(b"\r\n\r\nabc")


def test_u8_response_has_content_length():
    resp = Response(status=200, body=b"Hello")
    data = serialize_response(resp)
    assert b"Content-Length: 5\r\n" in data
    assert data.startswith(b"HTTP/1.1 200 OK\r\n")


def test_u8b_no_duplicate_content_length():
    resp = Response(status=200, headers={"Content-Length": "999"}, body=b"x")
    data = serialize_response(resp)
    assert data.count(b"Content-Length") == 1
    assert b"Content-Length: 999" in data


def test_u8c_date_present():
    resp = Response(status=200, body=b"")
    data = serialize_response(resp)
    assert b"Date: " in data


def test_u8d_unknown_status_reason_empty():
    resp = Response(status=599, body=b"")
    data = serialize_response(resp)
    assert data.startswith(b"HTTP/1.1 599 \r\n")
