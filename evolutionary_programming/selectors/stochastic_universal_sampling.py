import random
from typing import Sequence, Iterable, Tuple, Generic, TypeVar

from evolutionary_programming.details import Comparable
from evolutionary_programming.selectors.selector import IndividualType


class ScorableComparable(Comparable):
    def __float__(self) -> float:
        ...


ScoreType = TypeVar("ScoreType", bound=ScorableComparable)


class StochasticUniversalSampling(Generic[IndividualType, ScoreType]):
    def __init__(self, *, selection_size: int):
        self.selection_size = selection_size

    def __call__(
        self, population: Sequence[Tuple[IndividualType, ScoreType]]
    ) -> Iterable[IndividualType]:
        total_population_fitness_score = sum(float(i[1]) for i in population) or 1
        pointers_distance = total_population_fitness_score / self.selection_size
        start = random.uniform(0, pointers_distance)
        selected_points = [
            start + pointers_distance * i for i in range(self.selection_size)
        ]
        total_seen_score: float = 0.0
        for individual, score in population:
            cumulative_mating_probability = float(score) + total_seen_score
            while (
                selected_points
                and total_seen_score
                <= selected_points[0]
                < cumulative_mating_probability
            ):
                selected_points.pop()
                yield individual

            if not selected_points:
                return

            total_seen_score = cumulative_mating_probability
