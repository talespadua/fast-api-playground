import logging
import traceback


class Logger:
    def __init__(self) -> None:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # create file handler which logs even debug messages
        fh = logging.FileHandler("project.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        root_logger.addHandler(fh)

        # create console handler for info level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)

    def info(self, message: str) -> None:
        logging.info(message)

    def debug(self, message: str) -> None:
        logging.debug(message)

    def warning(self, message: str) -> None:
        logging.warning(message)

    def error(self) -> None:
        tb = traceback.format_exc()
        logging.error(tb)

    def critical(self, message: str) -> None:
        # TODO: Log to slack channel
        logging.critical(message)
