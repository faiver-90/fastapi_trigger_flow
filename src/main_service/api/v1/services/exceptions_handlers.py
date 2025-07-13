import json
import logging
from functools import wraps
from fastapi.responses import JSONResponse
from typing import Type, Callable, Dict

logger = logging.getLogger(__name__)


class ExceptionHandlerFactory:
    def __init__(self):
        self._handlers: Dict[
            Type[Exception],
            Callable[[Exception], JSONResponse]] = {}

    def register(self, exc_type: Type[Exception]):
        def decorator(handler_func: Callable[[Exception], JSONResponse]):
            self._handlers[exc_type] = handler_func
            return handler_func

        return decorator

    def get_handler(self,
                    exc: Exception,
                    default_status_code: int) -> JSONResponse:
        for exc_type, handler in self._handlers.items():
            if isinstance(exc, exc_type):
                return handler(exc)

        logger.exception("Unhandled exception in handler factory: %s", exc)
        return JSONResponse(
            status_code=default_status_code,
            content={
                "status": "error",
                "code": default_status_code,
                "message": f"Internal server error: {str(exc)}",
                "from": "handle_internal_errors"
            }
        )


exception_handler_factory = ExceptionHandlerFactory()


@exception_handler_factory.register(KeyError)
def handle_key_error(exc: KeyError):
    logger.error(f"KeyError: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "code": 400,
            "message": f"Missing key: {exc}",
            "from": "handle_internal_errors"
        }
    )


@exception_handler_factory.register(json.JSONDecodeError)
def handle_json_decode_error(exc: json.JSONDecodeError):
    logger.error(f"JSONDecodeError: {exc}")
    return JSONResponse(
        status_code=502,
        content={
            "status": "error",
            "code": 502,
            "message": f"Invalid JSON from service: {exc}",
            "from": "handle_internal_errors"
        }
    )


@exception_handler_factory.register(TypeError)
def handle_type_error(exc: TypeError):
    logger.error(f"TypeError: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "code": 500,
            "message": f"Type mismatch: {exc}",
            "from": "handle_internal_errors"
        }
    )


def handle_internal_errors(default_status_code: int = 500):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                return exception_handler_factory.get_handler(
                    exc,
                    default_status_code)

        return wrapper

    return decorator
