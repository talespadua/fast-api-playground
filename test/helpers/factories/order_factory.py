from decimal import Decimal
from typing import cast

import factory  # type: ignore[import]
from dateutil.tz import UTC
from factory.fuzzy import (  # type: ignore[import]
    FuzzyInteger,
    FuzzyDecimal,
    FuzzyChoice,
    FuzzyDateTime
)
from datetime import datetime
from project.dal.models import OrderModel
from project.dtos.order import OrderInputDTO


class OrderModelFactory(factory.Factory):  # type: ignore
    class Meta:
        model = OrderModel

    id = factory.Sequence(lambda n: n + 1)
    code = FuzzyInteger(10000, 99999)
    value = FuzzyDecimal(100.00, 100000.00)
    retailer_document = str(FuzzyInteger(10000000000, 99999999999))
    status = FuzzyChoice(["Em Validação", "Aprovado"])
    created_at = FuzzyDateTime(datetime(2012, 1, 1, tzinfo=UTC))

    @factory.lazy_attribute  # type: ignore
    def cashback(self) -> Decimal:
        return cast(Decimal, self.value) * Decimal(0.10)


class OrderInputDTOFactory(factory.Factory):  # type: ignore
    class Meta:
        model = OrderInputDTO

    code = FuzzyInteger(10000, 99999)
    value = FuzzyDecimal(100.00, 100000.00)
    retailer_document = str(FuzzyInteger(10000000000, 99999999999))
