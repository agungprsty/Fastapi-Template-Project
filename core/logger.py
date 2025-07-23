# Source: https://betterstack.com/community/guides/logging/logging-with-fastapi/

import os
import json
import logging
from datetime import datetime
from fastapi import FastAPI, Request
from logging.config import dictConfig

SENSITIVE_FIELDS = ["password", "access_token"]

def mask_sensitive_data(data: dict, fields: list[str]) -> dict:
    masked = data.copy()
    for field in fields:
        if field in masked:
            masked[field] = "***"
    return masked

# JSON Formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        if hasattr(record, "req"):
            log_record["req"] = record.req
        if hasattr(record, "res"):
            log_record["res"] = record.res

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def configure_logging(app: FastAPI):
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "http.log")

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "json",
                "stream": "ext://sys.stdout"
            },
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": log_path,
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5
            }
        },
        "loggers": {
            "": {
                "handlers": ["console", "rotating_file"],
                "level": "INFO"
            }
        }
    }

    dictConfig(log_config)
    logger = logging.getLogger(__name__)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        try:
            body_bytes = await request.body()
            body_str = body_bytes.decode("utf-8")
            body_json = json.loads(body_str) if body_str else None
            
            if isinstance(body_json, dict):
                body_json = mask_sensitive_data(body_json, SENSITIVE_FIELDS)
        except Exception:
            body_json = "non-JSON body"

        try:
            response = await call_next(request)
            log_extra = {
                "request_line": f"{request.method} {request.url.path}",
                "client_addr": request.client.host,
                "status_code": response.status_code,
                "req": {
                    "method": request.method,
                    "url": str(request.url),
                    "body": body_json,
                },
            }
        except Exception as exc:
            logger.error(
                "Unhandled exception occurred",
                exc_info=True,
                extra={
                    "request_line": f"{request.method} {request.url.path}",
                    "client_addr": request.client.host,
                    "req": {
                        "method": request.method,
                        "url": str(request.url),
                        "body": body_json,
                    },
                }
            )
            raise exc

        logger.info(
            "Request handled",
            extra=log_extra,
        )
        return response
