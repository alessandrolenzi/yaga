from typing import Generic, TypeVar, Iterable, Tuple, TYPE_CHECKING
from typing_extensions import Final
from evolutionary_algorithm.details import Comparable
from evolutionary_algorithm.genes.gene_definition import GeneType

from evolutionary_algorithm.individuals import IndividualType

if TYPE_CHECKING:
    from evolutionary_algorithm.evolutionary_algorithm import EvolutionaryAlgorithm

ScoreType = TypeVar("ScoreType", bound=Comparable)


class Evolution(Generic[IndividualType, GeneType, ScoreType]):
    def __init__(
        self,
        evolutionary_algorithm: "EvolutionaryAlgorithm[IndividualType, GeneType, ScoreType]",
    ):
        self._evolutionary_algorithm: Final = evolutionary_algorithm

    @property
    def population(self) -> Iterable[IndividualType]:
        for individual, score in self.scored_population:
            yield individual

    @property
    def scored_population(self) -> Iterable[Tuple[IndividualType, ScoreType]]:
        for individual, score in self._evolutionary_algorithm.ranker.ranked_population:
            yield individual, score

    @property
    def current_iteration(self) -> int:
        return self._evolutionary_algorithm._iterations

    @property
    def fittest(self):
        return self._evolutionary_algorithm.ranker.ranked_population[0][0]

    @property
    def fittest_score(self):
        return self._evolutionary_algorithm.ranker.ranked_population[0][1]

    def stop(self):
        self._evolutionary_algorithm.stop()
