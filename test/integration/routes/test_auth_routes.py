from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient
from project.main import app

client = TestClient(app)


@pytest.mark.usefixtures("create_tables")
class TestAuthRoutes:
    @pytest.fixture
    def auth_data(self) -> Dict[str, str]:
        return {"email": "sherolero@gmail.com", "password": "123456"}

    @pytest.fixture()
    def retailer_json(self) -> Dict[str, Any]:
        return {
            "full_name": "sherolero leroshero",
            "document": "123.456.789-25",
            "email": "sherolero@gmail.com",
            "password": "654321",
        }

    class TestGivenRetailerDoesNotExist:
        def test_its_unauthorized(self, auth_data: Dict[str, str]) -> None:
            response = client.post("/auth/token/", json=auth_data)
            assert response.status_code == 401

    class TestGivenRetailerExist:
        class TestWhenPasswordIsWrong:
            def test_its_unauthorized(
                self,
                retailer_json: Dict[str, Any],
                auth_data: Dict[str, str]
            ) -> None:
                client.post("/retailer/", json=retailer_json)
                response = client.post("/auth/token/", json=auth_data)
                assert response.status_code == 401

        class TestWhenPasswordIsCorrect:
            @pytest.fixture()
            def auth_data(self) -> Dict[str, str]:
                return {"email": "sherolero@gmail.com", "password": "654321"}

            def test_get_access_token(self, auth_data: Dict[str, str]) -> None:
                response = client.post("/auth/token/", json=auth_data)
                assert response.status_code == 200
