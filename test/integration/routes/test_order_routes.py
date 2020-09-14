import json
from typing import Dict, Any

import pytest

from fastapi.testclient import TestClient

from project.main import app
from project.services.order_service import OrderStatus
from project.services.order_service.order_service import ALLOWED_DOCUMENT_LIST

client = TestClient(app)


@pytest.mark.usefixtures("create_tables")
class TestOrderRoutes:
    @pytest.fixture()
    def retailer_json(self) -> Dict[str, Any]:
        return {
            "full_name": "sherolero leroshero",
            "document": "123.456.789-25",
            "email": "sherolero@gmail.com",
            "password": "123546",
        }

    @pytest.fixture()
    def order_json(self) -> Dict[str, Any]:
        return {"code": "123456", "value": "500", "retailer_document": "123.456.789-25"}

    class TestGivenInsertingOrder:
        class TestWhenThereIsNoOrders:
            def test_get_order_returns_empty(self, auth_token: Dict[str, str]) -> None:
                get_response = client.get("/order/", headers=auth_token)
                response_payload = json.loads(get_response.text)

                assert get_response.status_code == 200
                assert len(response_payload) == 0

        class TestWhenInsertingNewOrder:
            def test_insert_is_successful(
                self,
                order_json: Dict[str, Any],
                retailer_json: Dict[str, Any],
                auth_token: Dict[str, str],
            ) -> None:
                client.post("/retailer/", json=retailer_json)
                insert_response = client.post(
                    "/order/", json=order_json, headers=auth_token
                )
                assert insert_response.status_code == 201

        class TestWhenThereIsOrder:
            def test_get_order_finds_existing_order(
                self, auth_token: Dict[str, str]
            ) -> None:
                get_response = client.get("/order/", headers=auth_token)
                response_payload = json.loads(get_response.text)

                assert get_response.status_code == 200
                assert len(response_payload) > 0

    class TestGivenUpdatingOrder:
        @pytest.fixture()
        def update_json(self) -> Dict[str, Any]:
            return {
                "code": "123456",
                "value": "5000",
                "retailer_document": "123.456.789-25",
            }

        def test_update_is_successful(
            self, update_json: Dict[str, Any], auth_token: Dict[str, str]
        ) -> None:
            response = client.put("/order/1/", json=update_json, headers=auth_token)
            assert response.status_code == 200

        class TestWhenThereIsNoOrder:
            def test_should_return_404(
                self, update_json: Dict[str, Any], auth_token: Dict[str, str]
            ) -> None:
                response = client.put(
                    "/order/99999/", json=update_json, headers=auth_token
                )
                assert response.status_code == 404

    class TestGivenDeletingOrder:
        class TestGivenThereIsOrderToDelete:
            def test_delete_order(self, auth_token: Dict[str, str]) -> None:
                response = client.delete("/order/1/", headers=auth_token)
                assert response.status_code == 200

        class TestGivenThereIsNoOrderToDelete:
            def test_delete_order_returns_404(self, auth_token: Dict[str, str]) -> None:
                response = client.delete("/order/1/", headers=auth_token)
                assert response.status_code == 404

    class TestGivenApprovedOrder:
        @pytest.fixture()
        def retailer_json(self) -> Dict[str, Any]:
            return {
                "full_name": "teste teste",
                "document": ALLOWED_DOCUMENT_LIST[0],
                "email": "sherolero@hotmail.com",
                "password": "123546",
            }

        @pytest.fixture()
        def order_json(self) -> Dict[str, Any]:
            return {
                "code": "123456",
                "value": "500",
                "retailer_document": ALLOWED_DOCUMENT_LIST[0],
            }

        @pytest.fixture()
        def add_approved_order(
            self,
            retailer_json: Dict[str, Any],
            order_json: Dict[str, Any],
            auth_token: Dict[str, str],
        ) -> None:
            client.post("/retailer/", json=retailer_json)
            client.post("/order/", json=order_json, headers=auth_token)

        @pytest.mark.usefixtures("add_approved_order")  # type: ignore
        def test_cannot_delete_approved_order(self, auth_token: Dict[str, str]) -> None:
            delete_response = client.delete("/order/2/", headers=auth_token)
            assert delete_response.status_code == 405

        def test_cannot_update_approved_order(
            self, order_json: Dict[str, Any], auth_token: Dict[str, str]
        ) -> None:
            update_response = client.put(
                "/order/2/", json=order_json, headers=auth_token
            )
            assert update_response.status_code == 405
