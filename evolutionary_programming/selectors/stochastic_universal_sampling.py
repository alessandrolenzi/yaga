import random
from typing import Sequence, Iterable

from evolutionary_programming.details import Comparable
from evolutionary_programming.selectors.selector import Selector, IndividualType


class ScorableComparable(Comparable):
    def __float__(self) -> float:
        ...


class StochasticUniversalSampling(Selector[IndividualType, ScorableComparable]):
    def __call__(
        self, population: Sequence[IndividualType]
    ) -> Iterable[IndividualType]:
        _scored = [(i, self._score_function(i)) for i in population]
        total_population_fitness_score = sum(float(i[1]) for i in _scored) or 1
        pointers_distance = total_population_fitness_score / self.selection_size
        start = random.uniform(0, pointers_distance)
        selected_points = [
            start + pointers_distance * i for i in range(self.selection_size)
        ]
        total_seen_score: float = 0.0
        for individual, score in _scored:
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
