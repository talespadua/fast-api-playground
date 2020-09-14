from datetime import timedelta
from typing import Generator, Dict

import pytest
from pydantic import EmailStr
from sqlalchemy.orm import Session  # type: ignore

from project.config import Config
from project.dal.retailer import RetailerRepository
from project.dtos.retailer import RetailerInputDTO
from project.logger import Logger
from project.dal.models import Base, RetailerModel
from project.dal.mysql_connection import MySqlConnection
from project.services import RetailerService
from project.services.auth.auth_service import AuthService
from test.helpers.factories.retailer_factory import RetailerModelFactory

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


@pytest.fixture(scope="class")
def auth_token(
    config: Config,
    logger: Logger,
) -> Generator[Dict[str, str], None, None]:
    retailer_repository = RetailerRepository(config, logger)
    auth_service = AuthService(config, logger, retailer_repository)

    reatailer_model = RetailerModel(
        full_name="Authenticated User",
        document="99899899899",
        email=EmailStr("authenticated@gmail.com"),
        password="authpassword"
    )

    retailer_repository.insert_retailer(reatailer_model)
    retailer = retailer_repository.get_retailer_by_email("authenticated@gmail.com")

    auth_token = auth_service.generate_access_token(
        {"sub": "authenticated@gmail.com"},
        expires_delta=timedelta(
            minutes=int(config.get_config("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
    )

    yield {"Authorization": f"Bearer {auth_token}"}
    if retailer:
        retailer_repository.delete_retailer(retailer.id)
