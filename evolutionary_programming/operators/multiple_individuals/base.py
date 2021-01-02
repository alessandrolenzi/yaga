from abc import abstractmethod
from typing import Iterable

from evolutionary_programming.individuals import IndividualType
from evolutionary_programming.operators.base import GeneticOperator, GeneType


class MultipleIndividualOperator(GeneticOperator[IndividualType, GeneType]):
    @abstractmethod
    def __call__(self, it: Iterable[IndividualType]) -> IndividualType:
        ...
