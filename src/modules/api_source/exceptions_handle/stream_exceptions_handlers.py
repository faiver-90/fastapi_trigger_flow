# import logging
# from fastapi import Request, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
#
# logger = logging.getLogger(__name__)
#
#
# # Обработка ошибок валидации (422)
# async def validation_exception_handler(request: Request,
#                                        exc: RequestValidationError):
#     logger.warning(f"[422] Validation error on {request.url}: {exc.errors()}")
#     return JSONResponse(
#         status_code=422,
#         content={
#             "status": "error",
#             "code": 422,
#             "message": "Validation failed",
#             "errors": exc.errors(),
#         },
#     )
#
#
# # Обработка HTTP ошибок (raise HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     logger.warning(
#         f"[{exc.status_code}] HTTPException on {request.url}: {exc.detail}")
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "status": "error",
#             "code": exc.status_code,
#             "message": exc.detail,
#         },
#     )
#
#
# # Обработка всех других исключений
# async def generic_exception_handler(request: Request, exc: Exception):
#     logger.exception(f"[500] Unhandled exception on {request.url}: {str(exc)}")
#     return JSONResponse(
#         status_code=500,
#         content={
#             "status": "error",
#             "code": 500,
#             "message": f"Internal server error {exc}",
#         },
#     )
