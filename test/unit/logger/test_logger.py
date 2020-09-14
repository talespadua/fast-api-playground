import pytest

from project.logger import Logger

@pytest.fixture()
def logger() -> Logger:
    return Logger()


def test_logger(logger: Logger) -> None:
    msg = "Any Message"
    logger.info(msg)
    logger.error()
    logger.critical(msg)
    logger.debug(msg)
    logger.warning(msg)
