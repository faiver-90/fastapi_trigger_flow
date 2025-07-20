from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from src.modules.auth.api.v1.auth_router import v1
from src.shared.exceptions_handle.stream_exceptions_handlers import validation_exception_handler, \
    http_exception_handler, generic_exception_handler


def get_app() -> FastAPI:
    app_init = FastAPI()

    @app_init.get(
        '/',
        summary="Проверка соединения с сервером",
        description="Тестовый endpoint для проверки работоспособности сервера и очереди задач Celery.",
        tags=["Сервис"]
    )
    async def test_connection():
        return {"It's": "work"}

    app_init.add_exception_handler(RequestValidationError, validation_exception_handler)
    app_init.add_exception_handler(HTTPException, http_exception_handler)
    app_init.add_exception_handler(Exception, generic_exception_handler)
    app_init.include_router(v1)

    return app_init


app = get_app()
