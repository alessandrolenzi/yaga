import random
from typing import (
    TypeVar,
    Generic,
    Sequence,
    Tuple,
    List,
    Iterable,
    Iterator,
    Optional,
    Callable,
)

from evolutionary_programming.details import Comparable
from evolutionary_programming.evolution_status import EvolutionStatus
from evolutionary_programming.individuals import IndividualStructure
from evolutionary_programming.operators.protocols import (
    MultipleIndividualOperatorProtocol,
    SingleIndividualOperatorProtocol,
)
from evolutionary_programming.ranker import IndividualType, Ranker
from evolutionary_programming.selectors.selector import Selector

GeneType = TypeVar("GeneType")
ScoreType = TypeVar("ScoreType", bound=Comparable)


class EvolutionaryAlgorithm(Generic[IndividualType, GeneType, ScoreType]):
    def __init__(
        self,
        *,
        population_size: int,
        generations: Optional[int],
        selector: Selector,
        ranker: Ranker[IndividualType, ScoreType],
        individual_structure: IndividualStructure[IndividualType, GeneType],
        multiple_individual_operators: Sequence[
            Tuple[MultipleIndividualOperatorProtocol[IndividualType], float]
        ],
        single_individual_operators: Sequence[
            Tuple[SingleIndividualOperatorProtocol[IndividualType], float]
        ],
        iteration_callbacks: Optional[
            Sequence[Callable[["EvolutionStatus"], None]]
        ] = None,
        elite_size: int = 0,
    ):
        if population_size <= 0:
            raise ValueError(
                f"Invalid configuration: population size must be greather than 0. Specified {population_size}"
            )
        if generations is not None and generations <= 0:
            raise ValueError(
                f"Invalid configuration: cannot run for less than a generation. Specified {generations}"
            )
        self.population_size = population_size
        self.generations = generations
        self.ranker = ranker
        self.selector = selector
        self.individual_structures = individual_structure
        self.multiple_individual_operator = multiple_individual_operators
        self.single_individual_operator = single_individual_operators
        self.elite_size = elite_size
        self._iterations = 0
        self._stop = False
        self._population: List[IndividualType] = []
        self.iterations_callback = iteration_callbacks or []

    def set_initial_population(
        self, initial_population_iterator: Iterable[IndividualType]
    ):
        self._population = []
        for individual in initial_population_iterator:
            if len(self._population) == self.population_size:
                return
            self._population.append(individual)

    def ensure_population_initialized(self):
        while len(self._population) < self.population_size:
            self._population.append(self.individual_structures.build())

    def run(self):
        self.ensure_population_initialized()
        self._stop = False
        self._iterations = 0
        while not self._should_stop():
            self.perform_iteration()
            self.execute_callbacks()
        return self.ranker.ranked_population[0]

    def execute_callbacks(self):
        status = EvolutionStatus(self)
        for callback in self.iterations_callback:
            callback(status)

    def perform_iteration(self):
        self.ranker.rank(self._population)
        selected = list(self.selector(self.ranker.ranked_population))
        self._population = self.pick_elites(self.ranker.ranked_population)
        self._population += list(self._new_generation(selected))
        self._iterations += 1

    def pick_elites(
        self, ranked_population: Sequence[Tuple[IndividualType, ScoreType]]
    ):
        return [individual[0] for individual in ranked_population[: self.elite_size]]

    def _new_generation(
        self, parents: Sequence[IndividualType]
    ) -> Iterator[IndividualType]:
        for _ in range(self.population_size - self.elite_size):
            yield self._generate_individual(parents)

    def _generate_individual(self, parents: Sequence[IndividualType]) -> IndividualType:
        individual = parents[random.randint(0, len(parents) - 1)]
        for m_op, probability in self.multiple_individual_operator:
            if random.random() < probability:
                individual = m_op(individual, parents)
        for s_op, probability in self.single_individual_operator:
            if random.random() < probability:
                individual = s_op(individual)

        return individual

    def _should_stop(self):
        return self._stop or (
            self.generations is not None and self._iterations >= self.generations
        )

    @property
    def fittest_individual(self):
        return self.ranker.ranked_population[0][0]

    @property
    def best_score(self):
        return self.ranker.ranked_population[0][1]

    def stop(self):
        self._stop = True
