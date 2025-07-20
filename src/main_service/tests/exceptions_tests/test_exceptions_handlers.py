import json
import pytest
from fastapi.responses import JSONResponse

from src.main_service.api.v1.services.exceptions_handlers import exception_handler_factory, handle_internal_errors


def raise_value_error():
    raise ValueError("Test value error")


def raise_key_error():
    raise KeyError("missing_key")


def raise_json_decode_error():
    raise json.JSONDecodeError("Expecting value", "doc", 0)


def raise_type_error():
    raise TypeError("Wrong type")


@pytest.mark.parametrize(
    "exception_func, expected_status, expected_from",
    [
        (raise_value_error, 400, "handle_value_error"),
        (raise_key_error, 400, "handle_key_error"),
        (raise_json_decode_error, 502, "handle_json_decode_error"),
        (raise_type_error, 500, "handle_type_error"),
    ]
)
def test_registered_exception_handlers(exception_func, expected_status, expected_from):
    try:
        exception_func()
    except Exception as exc:
        response: JSONResponse = exception_handler_factory.get_handler(exc, default_status_code=500)

        assert isinstance(response, JSONResponse)
        assert response.status_code == expected_status

        payload = json.loads(response.body.decode())

        assert payload["from"] == expected_from
        assert payload["code"] == expected_status
        assert payload["status"] == "error"


def test_unhandled_exception_returns_default_response():
    class CustomException(Exception):
        pass

    exc = CustomException("Unknown error")
    response: JSONResponse = exception_handler_factory.get_handler(exc, default_status_code=503)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 503
    assert b"Internal server error" in response.body


@pytest.mark.asyncio
async def test_handle_internal_errors_decorator():
    @handle_internal_errors(default_status_code=499)
    async def faulty():
        raise ValueError("some value error")

    response: JSONResponse = await faulty()
    assert response.status_code == 400
    assert b"handle_value_error" in response.body
