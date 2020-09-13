import json

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from project.libs.cashback_client import CashbackClient
from project.main import app

client = TestClient(app)


class TestCashBackRoutes:
    def test_cashback_credit(self) -> None:
        response = client.get("/cashback/credit/12312312323/")
        response_payload = json.loads(response.text)

        assert response.status_code == 200
        assert response_payload["credit"]

    class TestWhenClientIsDead:
        def test_route_raises_503(self) -> None:
            fun_mock = MagicMock(return_value=None)
            with patch.object(CashbackClient, "get_cashback_credit", fun_mock):
                response = client.get("/cashback/credit/123")
                assert response.status_code == 503
