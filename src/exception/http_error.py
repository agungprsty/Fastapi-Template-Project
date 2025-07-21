class HttpException(Exception):
    def __init__(self, message=None, code=None, detail=None) -> None:
        self.http_response_status = getattr(self, "http_response_status", 500)
        self.code = code or getattr(self, "code", "internal_server_error")
        self.message = message or getattr(self, "message", "Internal Server Error")
        self.payload = {}

        if detail:
            self.payload["detail"] = detail

        super().__init__(self.message)

    def to_dict(self) -> dict:
        response = {
            "status": self.http_response_status,
            "code": self.code,
            "message": self.message,
        }
        if "detail" in self.payload:
            response["detail"] = self.payload["detail"]
        return {"meta": response}


class InternalServerErrorException(HttpException):
    message = "Internal Server Error"
    http_response_status = 500
    code = "internal_server_error"


class NotFoundException(HttpException):
    message = "Not Found"
    http_response_status = 404
    code = "not_found"


class UnauthorizedException(HttpException):
    message = "Unauthorized"
    http_response_status = 401
    code = "unauthorized"


class ForbiddenException(HttpException):
    message = "Forbidden"
    http_response_status = 403
    code = "forbidden"


class ConflictException(HttpException):
    message = "Conflict"
    http_response_status = 409
    code = "conflict"


class BadRequestException(HttpException):
    message = "Bad Request"
    http_response_status = 400
    code = "bad_request"


class TooManyRequestException(HttpException):
    message = "Too Many Requests"
    http_response_status = 429
    code = "too_many_request"

    def get_error(self) -> dict:
        return self.payload.get("detail", {})
