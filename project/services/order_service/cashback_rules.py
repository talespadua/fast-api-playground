from abc import ABC, abstractmethod
from decimal import Decimal


class BaseRule(ABC):
    @abstractmethod
    def accept(self, value: Decimal) -> bool:
        ...

    @abstractmethod
    def calculate_cashback(self, value: Decimal) -> Decimal:
        ...


class TenPercentRule(BaseRule):
    def accept(self, value: Decimal) -> bool:
        return value < 1000

    def calculate_cashback(self, value: Decimal) -> Decimal:
        return round(value * Decimal(0.1), 2)


class FifteenPercentRule(BaseRule):
    def accept(self, value: Decimal) -> bool:
        return 1000 <= value < 1500

    def calculate_cashback(self, value: Decimal) -> Decimal:
        return round(value * Decimal(0.15), 2)


class TwentyPercent(BaseRule):
    def accept(self, value: Decimal) -> bool:
        return value >= 1500

    def calculate_cashback(self, value: Decimal) -> Decimal:
        return round(value * Decimal(0.2), 2)


CASHBACK_RULES = [TenPercentRule(), FifteenPercentRule(), TwentyPercent()]
