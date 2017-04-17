import os
import inspect
import logging
import logging.handlers
from montagne import cfg

_DEFAULT_LOG_DATE_FORMAT = None
_DEFAULT_LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s]%(message)s"

_loggers = {}

CONF = cfg.CONF
CONF.register_cli_opts([
    cfg.IntOpt('log-level', default=20,
               help='set log level, default level INFO (with value 20).'),
    cfg.BoolOpt('verbose', default=False, help='show debug output'),
    cfg.StrOpt('log-dir', default=None, help='log file directory'),
    cfg.StrOpt('log-file', default=None, help='log file name'),
    cfg.StrOpt('log-file-mode', default='0644',
               help='default log file permission'),
])


def init_log():
    log = logging.getLogger()
    log_file = _get_log_file()
    if log_file is not None:
        wt_hdlr = logging.handlers.WatchedFileHandler(log_file)
        wt_hdlr.setFormatter(logging.Formatter(
            fmt=_DEFAULT_LOG_FORMAT,
            datefmt=_DEFAULT_LOG_DATE_FORMAT))
        log.addHandler(wt_hdlr)
        mode = int(CONF.log_file_mode, 8)
        os.chmod(log_file, mode)

    if CONF.log_level:
        log.setLevel(CONF.log_level)
    elif CONF.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


def getLogger(name=None):
    if name not in _loggers:
        logger = logging.getLogger(name)
        logger.propagate = False
        stream_hldr = logging.StreamHandler()
        stream_hldr.setFormatter(logging.Formatter(
            fmt=_DEFAULT_LOG_FORMAT,
            datefmt=_DEFAULT_LOG_DATE_FORMAT))
        logger.addHandler(stream_hldr)

        log_file = _get_log_file()
        if log_file is not None:
            wt_hdlr = logging.handlers.WatchedFileHandler(log_file)
            wt_hdlr.setFormatter(logging.Formatter(
                fmt=_DEFAULT_LOG_FORMAT,
                datefmt=_DEFAULT_LOG_DATE_FORMAT))
            logger.addHandler(wt_hdlr)
            mode = int(CONF.log_file_mode, 8)
            os.chmod(log_file, mode)

        if CONF.log_level:
            logger.setLevel(CONF.log_level)
        elif CONF.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        _loggers[name] = logger

    return _loggers[name]


def _get_log_file():
    if CONF.log_file:
        return CONF.log_file
    if CONF.log_dir:
        return os.path.join(CONF.log_dir,
                            os.path.basename(inspect.stack()[-1][1])) + '.log'
    return None
