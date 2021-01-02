import random
from typing import Iterable, Sequence, Tuple, Set, TypeVar, Generic

from evolutionary_programming.details import Comparable
from evolutionary_programming.selectors.selector import IndividualType, Selector, T

ScoreType = TypeVar("ScoreType", bound=Comparable)


class Random(Generic[IndividualType, ScoreType]):
    def __init__(self, selection_size: int):
        self.selection_size = selection_size

    def __call__(
        self, population: Sequence[Tuple[IndividualType, ScoreType]]
    ) -> Iterable[IndividualType]:
        unique_indexes = self.make_unique_indexes(len(population))
        for i in unique_indexes:
            yield population[i][0]

    def make_unique_indexes(self, pop_size) -> Set[int]:
        unique_indexes = set(
            random.randint(0, pop_size - 1) for _ in range(self.selection_size)
        )
        while len(unique_indexes) < self.selection_size:
            unique_indexes.add(random.randint(0, pop_size - 1))
        return unique_indexes
