import logging

from fortuna.config import CONFIG

_logger: logging.Logger | None = None


def configure_logger():
    logging.basicConfig(
        level=CONFIG.loglevel,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
    )


def get_logger():
    global _logger
    if _logger is None:
        configure_logger()
        _logger = logging.getLogger("fortuna")
    return _logger
