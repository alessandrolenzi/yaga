import random
from typing import Sequence, Tuple, Iterable

from evolutionary_programming.selectors.selector import Selector, \
    IndividualType


class Tournament(Selector[IndividualType]):
    def __init__(self, *, tournament_size: int, selection_size: int):
        super().__init__(selection_size)
        self.tournament_size = tournament_size

    def __call__(self, population: Sequence[Tuple[IndividualType, float]]) -> Iterable[IndividualType]:
        for _ in range(self.selection_size):
            tournament_individuals = [population[random.randint(0, len(population)-1)] for _ in range(self.tournament_size)]
            yield max(tournament_individuals, key=lambda individual_with_score: individual_with_score[1])[0]