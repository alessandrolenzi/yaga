import random
from typing import Tuple, Iterable, Sequence

from evolutionary_programming.selectors.selector import IndividualType, Selector


class Random(Selector[IndividualType]):
    def __call__(
        self, population: Sequence[Tuple[IndividualType, float]]
    ) -> Iterable[IndividualType]:
        unique_indexes = set(
            random.randint(0, len(population) - 1) for _ in range(self.selection_size)
        )
        while len(unique_indexes) < self.selection_size:
            unique_indexes.add(random.randint(0, len(population) - 1))

        for i in unique_indexes:
            yield population[i][0]
