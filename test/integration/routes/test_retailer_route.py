from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient
from project.main import app

client = TestClient(app)


@pytest.mark.usefixtures("create_tables")
class TestRetailerRoutes:
    @pytest.fixture()
    def retailer_json(self) -> Dict[str, Any]:
        return {
            "full_name": "sherolero leroshero",
            "document": "123546789",
            "email": "sherolero@gmail.com",
            "password": "123546",
        }

    class TestGivenInsertRetailer:
        class TestWhenPayloadIsValid:
            def test_insert_is_successfull(self, retailer_json: Dict[str, Any]) -> None:
                response = client.post("/retailer/", json=retailer_json)
                assert response.status_code == 201

        class TestWhenThereIsPayloadConflict:
            def test_insert_is_successfull(self, retailer_json: Dict[str, Any]) -> None:
                response = client.post("/retailer/", json=retailer_json)
                assert response.status_code == 405

    class TestGivenGetRetailer:
        class TestWhenRetailerExists:
            def test_response_should_be_ok(self) -> None:
                response = client.get(f"/retailer/1/")
                assert response.status_code == 200

        class TestWhenRetailerDontExist:
            def test_response_is_404(self) -> None:
                response = client.get("/retailer/99999999999/")
                assert response.status_code == 404
