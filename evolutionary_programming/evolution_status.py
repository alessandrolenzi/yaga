from typing import Generic, TypeVar, Iterable, Tuple, TYPE_CHECKING
from typing_extensions import Final
from evolutionary_programming.details import Comparable
from evolutionary_programming.genes.gene_definition import GeneType

from evolutionary_programming.individuals import IndividualType

if TYPE_CHECKING:
    from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm

ScoreType = TypeVar("ScoreType", bound=Comparable)


class AlgorithmHandle(Generic[IndividualType, GeneType, ScoreType]):
    def __init__(
        self,
        evolutionary_algorithm: "EvolutionaryAlgorithm[IndividualType, GeneType, ScoreType]",
    ):
        self._evolutionary_algorithm: Final = evolutionary_algorithm

    def population(self) -> Iterable[IndividualType]:
        for individual, score in self.scored_population():
            yield individual

    def scored_population(self) -> Iterable[Tuple[IndividualType, ScoreType]]:
        for individual, score in self._evolutionary_algorithm.ranker.ranked_population:
            yield individual, score

    def current_iteration(self) -> int:
        return self._evolutionary_algorithm._iterations

    def fittest(self):
        return self._evolutionary_algorithm.ranker.ranked_population[0]

    def fittest_score(self):
        return self._evolutionary_algorithm.ranker.ranked_population[1]

    def stop(self):
        self._evolutionary_algorithm.stop()
