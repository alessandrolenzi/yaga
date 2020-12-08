import random
from typing import Tuple, Iterable, Sequence

from evolutionary_programming.selectors.selector import IndividualType, \
    Selector


class Random(Selector[IndividualType]):

    def __call__(self, population: Sequence[Tuple[IndividualType, float]]) -> Iterable[IndividualType]:
        for i in [population[random.randint(0, len(population)-1)] for _ in range(self.selection_size)]:
            yield i[0]
