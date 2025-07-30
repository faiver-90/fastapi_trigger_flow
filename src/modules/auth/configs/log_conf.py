from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_auth_logger():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[{asctime}] {levelname}: {name}: {message}",
                    "style": "{",
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                },
            },
            "handlers": {
                "app": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "app.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
                "errors": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "errors.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "ERROR",
                },
                "access": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "access.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
                "auth": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "auth.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "loggers": {
                "app": {"handlers": ["app"], "level": "DEBUG", "propagate": False},
                "access": {"handlers": ["access"], "level": "INFO", "propagate": False},
                "auth": {"handlers": ["auth"], "level": "INFO", "propagate": False},
                "errors": {
                    "handlers": ["errors"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
    )
