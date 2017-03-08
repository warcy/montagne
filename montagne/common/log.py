import logging


_DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_DEFAULT_LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s]%(message)s"

_loggers = {}


def getLogger(name=None):
    if name not in _loggers:
        logger = logging.getLogger(name)
        logger.propagate = False
        stream_hldr = logging.StreamHandler()
        stream_hldr.setFormatter(logging.Formatter(
            fmt=_DEFAULT_LOG_FORMAT,
            datefmt=_DEFAULT_LOG_DATE_FORMAT))
        logger.addHandler(stream_hldr)

        _loggers[name] = logger

    return _loggers[name]
