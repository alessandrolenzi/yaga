import itertools
from concurrent.futures._base import Executor
from typing import Generic, Optional, Sequence, Tuple, Iterable, TypeVar, Callable
from yaga_ga.evolutionary_algorithm.details import Comparable

Q = TypeVar("Q", bound=Comparable)
IndividualType = TypeVar("IndividualType")
ScoreFunctionT = Callable[[IndividualType], Q]


class Ranker(Generic[IndividualType, Q]):
    def __init__(
        self, evaluation_function: ScoreFunctionT, executor: Optional[Executor] = None
    ):
        self.executor = executor
        self.evaluation_function = evaluation_function
        self.ranked_population: Sequence[Tuple[IndividualType, Q]] = []

    def rank(self, it: Iterable[IndividualType]) -> Sequence[Tuple[IndividualType, Q]]:
        self.ranked_population = list(
            sorted(
                self._evaluate(it),
                key=lambda scored_individual: scored_individual[1],
                reverse=True,
            )
        )
        return self.ranked_population

    def _evaluate(
        self, it: Iterable[IndividualType]
    ) -> Iterable[Tuple[IndividualType, Q]]:
        if not self.executor:
            for i in it:
                yield i, self.evaluation_function(i)
        else:
            i1, i2 = itertools.tee(it)
            yield from zip(i1, self.executor.map(self.evaluation_function, i2))
