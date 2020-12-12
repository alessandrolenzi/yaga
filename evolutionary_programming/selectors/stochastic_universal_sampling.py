import random
from typing import Sequence, Tuple, Iterable

from evolutionary_programming.selectors.selector import Selector, IndividualType


class StochasticUniversalSampling(Selector[IndividualType]):
    def __call__(
        self, population: Sequence[Tuple[IndividualType, float]]
    ) -> Iterable[IndividualType]:
        total_population_fitness_score = sum(i[1] for i in population) or 1
        pointers_distance = total_population_fitness_score / self.selection_size
        start = random.uniform(0, pointers_distance)
        selected_points = [
            start + pointers_distance * i for i in range(self.selection_size)
        ]
        total_seen_score = 0
        for individual, score in population:
            cumulative_mating_probability = score + total_seen_score
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
