from contextlib import contextmanager

from sqlalchemy import create_engine  # type: ignore[import]
from sqlalchemy.engine import Engine  # type: ignore[import]
from sqlalchemy.orm import Session, sessionmaker  # type: ignore[import]

from project.config import Config
from project.logger import Logger


class MySqlConnection(object):
    def __init__(self, config: Config, logger: Logger) -> None:
        self.logger = logger
        self.config = config
        self._engine = self._create_engine()
        self._session_factory = sessionmaker(bind=self._engine)

    def _create_engine(self) -> Engine:
        host = self.config.get_config("DB_HOST")
        port = int(self.config.get_config("DB_PORT"))
        user = self.config.get_config("DB_USER")
        password = self.config.get_config("DB_PASSWORD")
        database = self.config.get_config("DB_DATABASE")

        pool_size = int(self.config.get_config("DB_CONNECTION_POOL_SIZE"))
        max_overflow = int(self.config.get_config("DB_CONNECTION_POOL_MAX_OVERFLOW"))
        timeout = int(self.config.get_config("DB_CONNECTION_POOL_TIMEOUT"))
        pool_recycle = int(self.config.get_config("DB_CONNECTION_POOL_RECYCLE"))

        self.logger.info("Connecting MySQL server {}:{}".format(host, port))

        database_url = f"mysql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(
            database_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=timeout,
            pool_recycle=pool_recycle,
        )

    @contextmanager
    def session(self) -> Session:
        session = self._session_factory()
        try:
            yield session
        finally:
            session.close()
