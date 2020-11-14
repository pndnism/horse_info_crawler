import logging

logging.basicConfig(
    format='%(asctime)s [%(levelname)s:%(lineno)s] [%(name)s] %(message)s',
    level=logging.INFO)

LOGGER = logging.getLogger('application_logger')


def debug(*args, **kwargs):
    LOGGER.debug(*args, **kwargs)


def info(*args, **kwargs):
    LOGGER.info(*args, **kwargs)


def warning(*args, **kwargs):
    LOGGER.warning(*args, **kwargs)


def error(*args, **kwargs):
    # error レベルのログはスタックトレースを吐き出す
    LOGGER.error(exc_info=True, *args, **kwargs)