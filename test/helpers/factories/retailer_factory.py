import factory  # type: ignore[import]
from factory.fuzzy import FuzzyText  # type: ignore[import]

from project.dal.models import RetailerModel
from project.dtos.retailer import RetailerInputDTO


class RetailerModelFactory(factory.Factory):  # type: ignore
    class Meta:
        model = RetailerModel

    id = factory.Sequence(lambda n: n + 1)
    full_name = factory.Faker("name")
    document = factory.fuzzy.FuzzyText()
    email = factory.Faker("email")
    password = factory.fuzzy.FuzzyText(length=30)


class RetailerInputDtoFactory(factory.Factory):  # type: ignore
    class Meta:
        model = RetailerInputDTO

    full_name = factory.Faker("name")
    document = factory.fuzzy.FuzzyText()
    email = factory.Faker("email")
    password = factory.fuzzy.FuzzyText(length=30)
