from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException


from src.main_service.api.v1.auth_router import v1
from src.main_service.api.v1.services.stream_exceptions_handlers import validation_exception_handler, \
    http_exception_handler, generic_exception_handler


def get_app() -> FastAPI:
    import src.main_service.api.v1.configs.log_conf

    app = FastAPI()

    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)
    app.add_exception_handler(HTTPException,
                              http_exception_handler)
    app.add_exception_handler(Exception,
                              generic_exception_handler)
    app.include_router(v1)
    return app


app = get_app()
