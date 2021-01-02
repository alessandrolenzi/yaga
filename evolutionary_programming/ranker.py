from concurrent.futures._base import Executor
from typing import Generic, Optional, Sequence, Tuple, Iterable, TypeVar, Callable
from evolutionary_programming.details import Comparable

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
        self.ranked_population = list(self._evaluate(it))
        return sorted(
            self.ranked_population,
            key=lambda scored_individual: scored_individual[1],
            reverse=True,
        )

    def _evaluate(
        self, it: Iterable[IndividualType]
    ) -> Iterable[Tuple[IndividualType, Q]]:
        for i in it:
            yield i, self.evaluation_function(i)
