from typing import Generic, TypeVar

from typing_extensions import Final

from evolutionary_programming.individuals import IndividualStructure


class InvalidOperatorError(ValueError):
    pass


G = TypeVar("G")


class GeneticOperator(Generic[G]):
    def __init__(self, individual_structure: IndividualStructure[G]):
        self.individual_structure: Final = individual_structure
