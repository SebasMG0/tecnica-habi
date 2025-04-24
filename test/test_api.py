import json
from io import BytesIO
import pytest

from api.api import (
    BuildingsRESTHandler,
    STATUS_FILTER_CODES,
    QUERY_COLUMNS,
    set_response,
)

class FakeRequestHandler(BuildingsRESTHandler):
    def __init__(self, path, body=b"", headers=None, stop_on_error=True):
        """
        Initialize the fake request handler.
        Args:
            path (str): The request path.
            body (bytes): The request body.
            headers (dict): The request headers.
            stop_on_error (bool): Whether to stop on error or not.
        """

        self.path = path
        self.command = "GET"
        self.rfile = BytesIO(body)
        self.wfile = BytesIO()
        self.response_code = None
        self.error_code = None
        self.error_message = None
        self.stop_on_error = stop_on_error
        self.headers = headers if headers is not None else {}

    def send_response(self, code, message=None):
        self.response_code = code

    def send_error(self, code, message=None):
        self.error_code = code
        self.error_message = message
        if self.stop_on_error:
            raise Exception(f"Error {code}: {message}")

    def send_header(self, keyword, value):
        pass

    def end_headers(self):
        pass


def test_invalid_endpoint():
    """
        Test that if the endpoint is not found, it raises a 404 error.
    """

    handler = FakeRequestHandler("/otro_endpoint", body=b"", headers={"Content-Length": "0"})
    with pytest.raises(Exception) as excinfo:
        handler.do_GET()
    assert "404" in str(excinfo.value)
    assert "Endpoint is not found" in str(excinfo.value)


def test_invalid_json():
    """
        test that if the body is not valid JSON, it raises a 400 error.
    """
    body = b'invalid json'
    headers = {"Content-Length": str(len(body))}
    handler = FakeRequestHandler("/api/buildings", body= body, headers= headers, stop_on_error= True)
    with pytest.raises(Exception) as excinfo:
        handler.do_GET()
    assert "400" in str(excinfo.value)
    assert "The JSON body is not valid" in str(excinfo.value)


def test_execute_query_error(monkeypatch):
    """
        test that if execute_query raises a ValueError, send_error is called with code 400.
    """
    def fake_execute_query(status_filter_codes, filters, columns):
        raise ValueError("Test error in execute_query")

    
    monkeypatch.setattr("api.api.execute_query", fake_execute_query)

    handler = FakeRequestHandler("/api/buildings", body=b"", headers={"Content-Length": "0"})
    with pytest.raises(Exception) as excinfo:
        handler.do_GET()
    assert "400" in str(excinfo.value)
    assert "Test error in execute_query" in str(excinfo.value)


def test_valid_request_no_body(monkeypatch):
    """
        Test a valid request with no body.
    """
    dummy_result = {"data": "dummy result"}

    monkeypatch.setattr(
        "api.api.execute_query",
        lambda status_filter_codes, filters, columns: dummy_result
    )

    handler = FakeRequestHandler(
        "/api/buildings",
        body = b"",
        headers = {"Content-Length": "0"},
        stop_on_error = False
    )
    handler.do_GET()
    
    assert handler.response_code == 200
    
    output = handler.wfile.getvalue()
    result_json = json.loads(output.decode())
    assert result_json == dummy_result


def test_valid_request_with_body(monkeypatch):
    """
        Test a valid request with a valid body.
    """
    def fake_execute_query(status_filter_codes, filters, columns):
        """
            Simulate the behavior of execute_query
        """
        assert filters == {"city": "Bogota"}
        return {"result": "success"}

    monkeypatch.setattr("api.api.execute_query", fake_execute_query)

    body = json.dumps({"city": "Bogota"}).encode()
    headers = {"Content-Length": str(len(body))}
    handler = FakeRequestHandler(
        "/api/buildings", body=body, headers=headers, stop_on_error=False
    )
    handler.do_GET()
    
    assert handler.response_code == 200
    output = handler.wfile.getvalue()
    result_json = json.loads(output.decode())
    assert result_json == {"result": "success"}
