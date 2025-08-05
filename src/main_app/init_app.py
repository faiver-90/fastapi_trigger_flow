from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from src.modules.api_source.api.v1.notifications.notification_router import (
    v1_notification_router,
)
from src.modules.api_source.api.v1.source.source_router import v1_api_source
from src.modules.api_source.api.v1.trigger.trigger_router import v1_trigger_router
from src.modules.auth.api.v1.auth_router import v1_auth
from src.modules.auth.exceptions_handle.stream_exceptions_handlers import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)


def get_app() -> FastAPI:
    app_init = FastAPI(version="1.0.0")

    from sqlalchemy import text
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.shared.db.session import get_async_session

    @app_init.get(
        "/health_check",
        summary="Проверка работоспособности приложения и базы данных",
        description="Возвращает статус работы сервера и подключения к базе данных.",
        tags=["Service"],
    )
    async def health_check(session: AsyncSession = Depends(get_async_session)):
        try:
            await session.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        except SQLAlchemyError as e:
            return {"status": "error", "database": f"unavailable: {str(e)}"}

    # ================================================
    from fastapi import Body
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.shared.db.session import get_async_session

    @app_init.post("/run_for_source", tags=["Service"])
    async def run_for_source(
        temp: int = Body(...), session: AsyncSession = Depends(get_async_session)
    ):
        from src.shared.services.observe_trigger_notify_service import (
            TriggerExecutorService,
        )

        service = TriggerExecutorService(session)
        payloads = {1: {"temp": temp}}
        await service.run_for_all_sources(payloads)
        return {"result": "message send"}

    app_init.add_exception_handler(RequestValidationError, validation_exception_handler)
    app_init.add_exception_handler(HTTPException, http_exception_handler)
    app_init.add_exception_handler(Exception, generic_exception_handler)
    app_init.include_router(v1_auth)
    app_init.include_router(v1_api_source)
    app_init.include_router(v1_notification_router)
    app_init.include_router(v1_trigger_router)

    return app_init


app = get_app()
