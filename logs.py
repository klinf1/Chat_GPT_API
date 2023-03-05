import logging
from logging.handlers import RotatingFileHandler


def set_up_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(
        'logs.log',
        maxBytes=50000000,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(funcName)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
