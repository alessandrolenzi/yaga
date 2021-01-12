import random
from typing import Sequence, Iterable, Tuple, Generic, TypeVar, List

from evolutionary_algorithm.details import Comparable
from evolutionary_algorithm.selectors.selector import IndividualType


class FloatComparable(Comparable):
    def __float__(self) -> float:
        ...


ScoreType = TypeVar("ScoreType", bound=FloatComparable)


class StochasticUniversalSampling(Generic[IndividualType, ScoreType]):
    def __init__(self, *, selection_size: int):
        self.selection_size = selection_size

    def __call__(
        self, population: Sequence[Tuple[IndividualType, ScoreType]]
    ) -> Iterable[IndividualType]:
        total_population_fitness_score = sum(float(i[1]) for i in population) or 1
        selected_points = self.make_selection_points(total_population_fitness_score)
        total_seen_score: float = 0.0

        for individual, score in population:
            cumulative_selection_score = float(score) + total_seen_score
            while (
                selected_points
                and total_seen_score <= selected_points[0]
                and selected_points[0] < cumulative_selection_score
            ):
                selected_points.pop(0)
                yield individual
            total_seen_score = cumulative_selection_score

    def make_selection_points(
        self, total_population_fitness_score: float
    ) -> List[float]:
        pointers_distance = total_population_fitness_score / self.selection_size
        start = random.uniform(0, pointers_distance)
        return [start + pointers_distance * i for i in range(self.selection_size)]
