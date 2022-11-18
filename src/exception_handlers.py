from fastapi import Request, Response
from fastapi.responses import JSONResponse
from src.schemas import Error
from src.exceptions import CustomHTTPException, INVALID_REQUEST_EXCEPTION


async def custom_http_exception_handler(request: Request, exc: CustomHTTPException) -> Response:
    headers = getattr(exc, "headers", None)
    if exc.error is None:
        return Response(status_code=exc.status_code, headers=headers)
    
    return JSONResponse(
        {"error": exc.error, "error_description": exc.error_description}, 
        status_code=exc.status_code, 
        headers=headers
    )


async def validation_error_handler(request: Request, ex: Exception):
    return await custom_http_exception_handler(request, INVALID_REQUEST_EXCEPTION)
