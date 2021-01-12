import random
from typing import Sequence, Tuple, Iterable, Generic, TypeVar

from evolutionary_algorithm.details import Comparable
from evolutionary_algorithm.selectors.selector import IndividualType

ScoreType = TypeVar("ScoreType", bound=Comparable)


class Tournament(Generic[IndividualType, ScoreType]):
    def __init__(self, *, tournament_size: int, selection_size: int):
        self.tournament_size = tournament_size
        self.selection_size = selection_size

    def __call__(
        self, population: Sequence[Tuple[IndividualType, ScoreType]]
    ) -> Iterable[IndividualType]:
        for i in range(self.selection_size):
            tournament_individuals = self.pick_tournament_individuals(population)
            yield max(
                tournament_individuals,
                key=lambda individual_with_score: individual_with_score[1],
            )[0]

    def pick_tournament_individuals(
        self, population: Sequence[Tuple[IndividualType, ScoreType]]
    ) -> Sequence[Tuple[IndividualType, ScoreType]]:
        return [
            population[random.randint(0, len(population) - 1)]
            for _ in range(self.tournament_size)
        ]
