import random
from typing import Iterable, Sequence, Tuple
from evolutionary_programming.selectors.selector import IndividualType, Selector, T


class Random(Selector):
    def __call__(
        self, population: Sequence[Tuple[IndividualType, T]]
    ) -> Iterable[IndividualType]:
        unique_indexes = set(
            random.randint(0, len(population) - 1) for _ in range(self.selection_size)
        )
        while len(unique_indexes) < self.selection_size:
            unique_indexes.add(random.randint(0, len(population) - 1))

        for i in unique_indexes:
            yield population[i][0]
