from abc import abstractmethod
from functools import singledispatch
from typing import Iterable, List, cast

from typing_extensions import Final

from evolutionary_programming.individuals import IndividualType, IndividualStructure
from evolutionary_programming.operators.base import GeneticOperator, GeneType
from evolutionary_programming.utils.reservoir_sampling import random_selection


class MultipleIndividualOperator(GeneticOperator[IndividualType, GeneType]):
    def __init__(
        self,
        individual_structure: IndividualStructure[IndividualType, GeneType],
        arity: int = 2,
    ):
        super().__init__(individual_structure)
        self.arity: Final = arity

    @abstractmethod
    def __call__(
        self, selected: IndividualType, it: Iterable[IndividualType]
    ) -> IndividualType:
        ...

    def pick(
        self, selected: IndividualType, parents: Iterable[IndividualType]
    ) -> List[IndividualType]:
        return [selected] + cast(
            List[IndividualType], random_selection(parents, self.arity - 1)
        )
