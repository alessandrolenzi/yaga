from abc import abstractmethod
from typing import TypeVar

from evolutionary_programming.operators.base import GeneticOperator

IndividualType = TypeVar("IndividualType")
GeneType = TypeVar("GeneType")


class SingleIndividualOperator(GeneticOperator[IndividualType, GeneType]):
    @abstractmethod
    def __call__(self, _parent1: IndividualType) -> IndividualType:
        ...
