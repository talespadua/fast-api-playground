import factory  # type: ignore[import]
from factory.fuzzy import FuzzyText  # type: ignore[import]

from project.retailers.dto import RetailerInputDTO


class RetailerInputFactory(factory.Factory):  # type: ignore
    class Meta:
        model = RetailerInputDTO

    id = factory.Sequence(lambda n: n + 1)
    full_name = factory.Faker("name")
    document = factory.fuzzy.FuzzyText()
    email = factory.Faker("email")
    password = factory.fuzzy.FuzzyText(length=30)
