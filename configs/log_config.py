log_setting = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "formatter": "detail",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG"
        },
        "file": {
            "formatter": "standard",
            "filename": "crterbot.log",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG"
        },
        "socket": {
            "level": "DEBUG",
            "class": "logging.handlers.SocketHandler",
            "host": "127.0.0.1",
            "port": 8002,
            "formatter": "standard"
        },
        "http": {
            "level": "DEBUG",
            "class": "logging.handlers.HTTPHandler",
            "host": "127.0.0.1",
            "url": "/log",
            "method": "POST",
            "formatter": "standard"
        },
        "mail": {
            "level": "DEBUG",
            "class": "logging.handlers.SMTPHandler",
            "mailhost": "",
            "fromaddr": "",
            "toaddrs": "",
            "subject": "",
            "credentials": "",
            "formatter": "standard"
        }
    },
    "formatters": {
        "simple": {
            "format": "%(filename)s[line:%(lineno)d]%(levelname)s %(message)s"
        },
        "detail": {
            "format": "%(asctime)s %(filename)s[line:%(lineno)d]%(name)s %(levelname)s %(message)s"
        },
        "standard": {
            "format": "%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s"
        }
    },
    "root": {
        "level": "WARN",
        "propagate": False,
        "handlers": ["console", "file"]
    },
    "loggers": {
        "web": {
            "handlers": ["console", "file", "socket"],
            "propagate": False,
            "level": "DEBUG"
        }
    }
}
