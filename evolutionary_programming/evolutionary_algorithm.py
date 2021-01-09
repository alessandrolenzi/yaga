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
from evolutionary_programming.individuals import IndividualStructure
from evolutionary_programming.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_programming.operators.single_individual.base import (
    SingleIndividualOperator,
)
from evolutionary_programming.ranker import IndividualType, Ranker
from evolutionary_programming.selectors.selector import Selector

GeneType = TypeVar("GeneType")
T = TypeVar("T", bound=Comparable)


class EvolutionaryAlgorithm(Generic[IndividualType, GeneType, T]):
    def __init__(
        self,
        *,
        population_size: int,
        generations: Optional[int],
        selector: Selector,
        ranker: Ranker[IndividualType, T],
        individual_structure: IndividualStructure[IndividualType, GeneType],
        multiple_individual_operators: Sequence[
            Tuple[MultipleIndividualOperator[IndividualType, GeneType], float]
        ],
        single_individual_operators: Sequence[
            Tuple[SingleIndividualOperator[IndividualType, GeneType], float]
        ],
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
        self.iterations = 0
        self.population: List[IndividualType] = []

    def set_initial_population(
        self, initial_population_iterator: Iterable[IndividualType]
    ):
        self.population = []
        for individual in initial_population_iterator:
            if len(self.population) == self.population_size:
                return
            self.population.append(individual)

    def ensure_population_initialized(self):
        while len(self.population) < self.population_size:
            self.population.append(self.individual_structures.build())

    def run(self):
        self.ensure_population_initialized()
        while not self._should_stop():
            self.perform_iteration()
        return self.ranker.ranked_population[0]

    def perform_iteration(self):
        self.ranker.rank(self.population)
        selected = list(self.selector(self.ranker.ranked_population))
        self.population = self.pick_elites(self.ranker.ranked_population)
        self.population += list(self._new_generation(selected))

    def pick_elites(self, ranked_population: Sequence[Tuple[IndividualType, T]]):
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
        self.iterations += 1
        return self.generations is not None and self.iterations > self.generations
