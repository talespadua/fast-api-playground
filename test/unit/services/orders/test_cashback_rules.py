from decimal import Decimal
from typing import Any, cast

import pytest
from project.services.order_service.cashback_rules import (
    BaseRule,
    TenPercentRule,
    FifteenPercentRule,
    TwentyPercent
)


class BaseRuleBehavior:
    @pytest.fixture()
    def calculate_cashback(self, rule: BaseRule, value: Decimal) -> Decimal:
        return rule.calculate_cashback(value)

    def test_accept_value(self, rule: BaseRule, valid_value: Decimal) -> None:
        assert rule.accept(valid_value)

    def test_reject_value(self, rule: BaseRule, invalid_value: Decimal) -> None:
        assert not rule.accept(invalid_value)

    def test_calculate_cashback(
        self,
        calculate_cashback: Decimal,
        expected_cashback: Decimal
    ) -> None:
        assert calculate_cashback == expected_cashback


class TestTenPercentRule(BaseRuleBehavior):
    @pytest.fixture()
    def rule(self) -> BaseRule:
        return TenPercentRule()

    @pytest.fixture(params=[120.30, 800, 10.80])
    def valid_value(self, request: Any) -> Decimal:
        return Decimal(request.param)

    @pytest.fixture(params=[1201.30, 1000, 5000.80])
    def invalid_value(self, request: Any) -> Decimal:
        return Decimal(request.param)

    @pytest.fixture()
    def value(self) -> Decimal:
        return Decimal(100.00)

    @pytest.fixture()
    def expected_cashback(self) -> Decimal:
        return Decimal(10.00)


class TestFifteenPercentRule(BaseRuleBehavior):
    @pytest.fixture()
    def rule(self) -> BaseRule:
        return FifteenPercentRule()

    @pytest.fixture(params=[1200.30, 1499.99, 1000])
    def valid_value(self, request: Any) -> Decimal:
        return Decimal(request.param)

    @pytest.fixture(params=[830.30, 2000.00, 5000.80])
    def invalid_value(self, request: Any) -> Decimal:
        return Decimal(request.param)

    @pytest.fixture()
    def value(self) -> Decimal:
        return Decimal(100.00)

    @pytest.fixture()
    def expected_cashback(self) -> Decimal:
        return Decimal(15.00)


class TestTwentyPercent(BaseRuleBehavior):
    @pytest.fixture()
    def rule(self) -> BaseRule:
        return TwentyPercent()

    @pytest.fixture(params=[2000.30, 5000.99, 800000.55])
    def valid_value(self, request: Any) -> Decimal:
        return Decimal(request.param)

    @pytest.fixture(params=[830.30, 1400.00, 0.80])
    def invalid_value(self, request: Any) -> Decimal:
        return Decimal(request.param)

    @pytest.fixture()
    def value(self) -> Decimal:
        return Decimal(100.00)

    @pytest.fixture()
    def expected_cashback(self) -> Decimal:
        return Decimal(20.00)
