from typing import Generic, TypeVar

from typing_extensions import Final

from evolutionary_algorithm.individuals import IndividualStructure


class InvalidOperatorError(ValueError):
    pass


IndividualType = TypeVar("IndividualType")
GeneType = TypeVar("GeneType")


class GeneticOperator(Generic[IndividualType, GeneType]):
    def __init__(
        self, individual_structure: IndividualStructure[IndividualType, GeneType]
    ):
        self.individual_structure: Final = individual_structure
