import logging
from logging import config, getLogger

log_config = {
    "version":1,
    "root": {
        "handlers" : ["console"],
        "level": "DEBUG"
    },
    "handlers": {
        "console":{
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    },
    "loggers": {
        "sortinator": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "utils": {"level": "INFO", "handlers": ["console"]},
        "webserver": {"level": "INFO", "handlers": ["console"]},
        "celery.worker": {"level": "INFO", "handlers": ["console"], "propagate": False}
    }
}

config.dictConfig(log_config)


def get_logger(name):
    return getLogger(name)
