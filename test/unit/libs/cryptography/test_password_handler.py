import pytest
from project.libs.criptography.password_handler import (
    verify_password,
    get_password_hash
)


@pytest.fixture()
def raw_password() -> str:
    return "12345"


@pytest.fixture()
def hashed_password(raw_password: str) -> str:
    return get_password_hash(raw_password)


def test_password_is_being_hashed(raw_password: str, hashed_password: str) -> None:
    assert verify_password(raw_password, hashed_password)
