from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from api.v1.auth_router import v1
from api.v1.services import stream_exceptions_handlers


def get_app() -> FastAPI:
    import api.v1.configs.log_conf

    app = FastAPI()

    app.add_exception_handler(RequestValidationError,
                              stream_exceptions_handlers.validation_exception_handler)
    app.add_exception_handler(HTTPException,
                              stream_exceptions_handlers.http_exception_handler)
    app.add_exception_handler(Exception,
                              stream_exceptions_handlers.generic_exception_handler)
    app.include_router(v1)
    return app


app = get_app()
