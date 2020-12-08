from typing import Tuple, Iterable, Sequence

from evolutionary_programming.selectors.selector import Selector, \
    IndividualType


class Ranking(Selector[IndividualType]):
    def __call__(self, population: Sequence[Tuple[IndividualType, float]]) -> Iterable[IndividualType]:
        for i in sorted(population, key=lambda x: x[1], reverse=True)[:self.selection_size]:
            yield i[0]
