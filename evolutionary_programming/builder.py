from concurrent.futures._base import Executor
import random
from typing import (
    Final,
    Callable,
    TypeVar,
    Generic,
    Sequence,
    Iterator,
    Tuple,
    Iterable,
    List,
    Optional,
)

from evolutionary_programming.details import Comparable
from evolutionary_programming.individuals import IndividualStructure
from evolutionary_programming.individuals.individual_structure import G, IndividualType
from evolutionary_programming.operators.base import GeneticOperator
from evolutionary_programming.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_programming.operators.single_individual.base import (
    SingleIndividualOperator,
)
from evolutionary_programming.selectors.selector import Selector

Q = TypeVar("Q", bound=Comparable)
ScoreFunctionT = Callable[[IndividualType[G]], Q]


class Ranker(Generic[G, Q]):
    def __init__(
        self, evaluation_function: ScoreFunctionT, executor: Optional[Executor] = None
    ):
        self.executor = executor
        self.evaluation_function = evaluation_function
        self.ranked_population: Sequence[Tuple[IndividualType[G], Q]] = []

    def rank(
        self, it: Iterable[IndividualType[G]]
    ) -> Sequence[Tuple[IndividualType[G], Q]]:
        self.ranked_population = list(self._evaluate(it))
        return sorted(
            self.ranked_population,
            key=lambda scored_individual: scored_individual[1],
            reverse=True,
        )

    def _evaluate(
        self, it: Iterable[IndividualType[G]]
    ) -> Iterable[Tuple[IndividualType[G], Q]]:
        for i in it:
            yield i, self.evaluation_function(i)


T = TypeVar("T")


class EvolutionaryAlgorithmInstance(Generic[G, T]):
    def __init__(
        self,
        *,
        population_size: int,
        generations: int,
        selector: Selector[G, T],
        ranker: Ranker[G, T],
        individual_structure: IndividualStructure[G],
        multiple_individual_operators: Sequence[
            Tuple[MultipleIndividualOperator[G], float]
        ],
        single_individual_operators: Sequence[
            Tuple[SingleIndividualOperator[G], float]
        ],
        elite_size: int = 0,
    ):
        self.population_size = population_size
        self.generations = generations
        self.ranker = ranker
        self.selector = selector
        self.individual_structures = individual_structure
        self.multiple_individual_operator = multiple_individual_operators
        self.single_individual_operator = single_individual_operators
        self.elite_size = elite_size
        self.iterations = 0
        self.population = []

    def run(self):
        while len(self.population) < self.population_size:
            self.population.append(self.individual_structures.build())
        while not self._should_stop():
            self.population = list(self._new_generation(self.population))

    def _new_generation(
        self, population: Iterable[IndividualType]
    ) -> Iterator[IndividualType]:
        ranked_population = self.ranker.rank(population)
        parents = list(self.selector(ranked_population))
        print(f"the best is {ranked_population[0]}")
        for i in ranked_population[: self.elite_size]:
            yield i[0]
        for _ in range(self.population_size - self.elite_size):
            yield self._generate_individual(parents)

    def _generate_individual(
        self, parents: Sequence[Tuple[IndividualType, T]]
    ) -> IndividualType:
        individual = parents[random.randint(0, len(parents) - 1)]
        for operator, probability in self.multiple_individual_operator:
            if random.random() < probability:
                individual = operator(
                    [individual, parents[random.randint(0, len(parents) - 1)]]
                )
        for operator, probability in self.single_individual_operator:
            if random.random() < probability:
                individual = operator(individual)

        return individual

    def _should_stop(self):
        self.iterations += 1
        print(f"Iteration: {self.iterations}")
        return self.iterations >= self.generations


class EvolutionaryAlgorithmBuilder:
    population_size: Final[int]
    generations: Final[int]

    def __init__(
        self,
        population_size: int,
        generations: int,
        surviving_parents_portion: float = 0.8,
    ):
        self.population_size = population_size
        self.generations = generations
        self.surviving_parents = int(population_size * surviving_parents_portion)
        self._operators = []

    def individual_structure(self, i: IndividualStructure[G]):
        self._indstr = i
        return self

    def selector(self, s: Selector):
        self._selector = s
        return self

    def executor(self, e: Executor):
        self._executor = e
        return self

    def add_operator(
        self,
        operator_builder: Callable[[IndividualStructure[G]], GeneticOperator[G]],
        execution_probability: float,
    ):
        self._operators.append((operator_builder, execution_probability))
        return self

    def initialize(self, score_function: Callable[[IndividualType[G]], Q]):
        (
            multiple_individual_operators,
            single_individual_operators,
        ) = self._prepare_operators()
        return EvolutionaryAlgorithmInstance(
            population_size=self.population_size,
            generations=self.generations,
            individual_structure=self._indstr,
            ranker=Ranker(score_function),
            selector=self._selector,
            multiple_individual_operators=multiple_individual_operators,
            single_individual_operators=single_individual_operators,
        )

    def _prepare_operators(self):
        multiple_operators: List[Tuple[MultipleIndividualOperator, float]] = []
        single_operators: List[Tuple[SingleIndividualOperator, float]] = []
        for operator, prob in self._operators:
            concrete = operator(self._indstr)
            if isinstance(concrete, MultipleIndividualOperator):
                multiple_operators.append((concrete, prob))
            else:
                single_operators.append((concrete, prob))
        return multiple_operators, single_operators
