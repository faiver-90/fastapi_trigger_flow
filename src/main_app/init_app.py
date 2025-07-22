from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from src.modules.api_source.api.v1.notifications.crud_notification_template import v1_notification_router
from src.modules.api_source.api.v1.source.api_source_router.crud_source import v1_api_source
from src.modules.api_source.api.v1.trigger.crud_trigger import v1_trigger_router
from src.modules.api_source.api.v1.user_trigger_bindings.crud_user_trigger_binding import v1_user_trigger_binding_router
from src.modules.auth.api.v1.auth_router import v1_auth
from src.modules.auth.exceptions_handle.stream_exceptions_handlers import validation_exception_handler, \
    http_exception_handler, generic_exception_handler


def get_app() -> FastAPI:
    app_init = FastAPI(version="1.0.0")

    @app_init.get(
        '/',
        summary="Проверка соединения с сервером",
        description="Тестовый endpoint для проверки работоспособности сервера и очереди задач Celery.",
        tags=["Service"]
    )
    async def test_connection():
        return {"It's": "work"}

    app_init.add_exception_handler(RequestValidationError, validation_exception_handler)
    app_init.add_exception_handler(HTTPException, http_exception_handler)
    app_init.add_exception_handler(Exception, generic_exception_handler)
    app_init.include_router(v1_auth)
    app_init.include_router(v1_api_source)
    app_init.include_router(v1_notification_router)
    app_init.include_router(v1_trigger_router)
    app_init.include_router(v1_user_trigger_binding_router)

    return app_init


app = get_app()
