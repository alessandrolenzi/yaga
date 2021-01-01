from abc import abstractmethod
from typing import Iterable

from evolutionary_programming.individuals.individual_structure import (
    G,
    IndividualType,
)
from evolutionary_programming.operators.base import GeneticOperator


class MultipleIndividualOperator(GeneticOperator[G]):
    @abstractmethod
    def __call__(self, it: Iterable[IndividualType[G]]) -> IndividualType[G]:
        ...
