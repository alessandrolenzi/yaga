from typing import Iterable, Sequence

from evolutionary_programming.selectors.selector import Selector, IndividualType


class Ranking(Selector[IndividualType]):
    def __call__(
        self, population: Sequence[IndividualType]
    ) -> Iterable[IndividualType]:
        _pop = [(i, self._score_function(i)) for i in population]
        for i in sorted(_pop, key=lambda x: x[1], reverse=True)[: self.selection_size]:
            yield i[0]
