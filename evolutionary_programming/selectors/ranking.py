from typing import Iterable, Sequence, Tuple

from evolutionary_programming.selectors.selector import Selector, IndividualType, T


class Ranking(Selector):
    def __call__(
        self, population: Sequence[Tuple[IndividualType, T]]
    ) -> Iterable[IndividualType]:
        for i in sorted(population, key=lambda x: x[1], reverse=True)[
            : self.selection_size
        ]:
            yield i[0]
