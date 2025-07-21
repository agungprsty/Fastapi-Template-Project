from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from src.exception.http_error import HttpException

def http_exception_handler(request: Request, exc: HttpException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "error": {
                "type": "HttpException",
                "message": exc.message,
            },
        },
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "message": "Invalid request",
                "details": exc.errors(),
            }
        },
    )


def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc) or "Internal Server Error"
            }
        },
    )


def register_exception_handlers(app):
    """
    Fungsi untuk mendaftarkan semua custom exception handler ke FastAPI app
    """
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
