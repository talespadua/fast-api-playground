import json
import pytest
from typing import Dict
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from project.libs.cashback_client import CashbackClient
from project.main import app

client = TestClient(app)


@pytest.mark.usefixtures("create_tables")
class TestCashBackRoutes:
    def test_cashback_credit(self, auth_token: Dict[str, str]) -> None:
        response = client.get("/cashback/credit/12312312323/", headers=auth_token)
        response_payload = json.loads(response.text)

        assert response.status_code == 200
        assert response_payload["credit"]

    class TestWhenClientIsDead:
        def test_route_raises_503(self, auth_token: Dict[str, str]) -> None:
            fun_mock = MagicMock(return_value=None)
            with patch.object(CashbackClient, "get_cashback_credit", fun_mock):
                response = client.get("/cashback/credit/123", headers=auth_token)
                assert response.status_code == 503
