from abc import abstractmethod

from evolutionary_programming.individuals import IndividualType
from evolutionary_programming.operators.base import GeneticOperator, G


class SingleIndividualOperator(GeneticOperator[G]):
    @abstractmethod
    def __call__(self, _parent1: IndividualType[G]) -> IndividualType[G]:
        ...
