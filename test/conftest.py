from typing import Generator

import pytest
from sqlalchemy.orm import Session  # type: ignore

from project.config import Config
from project.logger import Logger
from project.dal.models import Base
from project.dal.mysql_connection import MySqlConnection

pytest_plugins = ["test.helpers.fixtures.config_fixtures"]


@pytest.fixture(scope="module")
def mysql_orm_connection(config: Config, logger: Logger) -> MySqlConnection:
    return MySqlConnection(config, logger)


@pytest.fixture(scope="module")
def db_session(mysql_orm_connection: MySqlConnection) -> Session:
    with mysql_orm_connection.session() as session:
        yield session


@pytest.fixture(scope="module")
def create_tables(
    mysql_orm_connection: MySqlConnection,
) -> Generator[None, None, None]:
    Base.metadata.create_all(bind=mysql_orm_connection._engine)
    yield
    Base.metadata.drop_all(bind=mysql_orm_connection._engine)
