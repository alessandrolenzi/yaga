from typing import Iterable, Sequence, Tuple, TypeVar, Generic

from evolutionary_algorithm.details import Comparable
from evolutionary_algorithm.individuals import IndividualType

ScoreType = TypeVar("ScoreType", bound=Comparable)


class Ranking(Generic[IndividualType, ScoreType]):
    def __init__(self, selection_size: int):
        self.selection_size = selection_size

    def __call__(
        self, population: Sequence[Tuple[IndividualType, ScoreType]]
    ) -> Iterable[IndividualType]:
        for i in population[: self.selection_size]:
            yield i[0]
