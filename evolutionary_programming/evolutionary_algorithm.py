import random
from typing import TypeVar, Generic, Sequence, Tuple, List, Iterable, Iterator

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


class EvolutionaryAlgorithmInstance(Generic[IndividualType, GeneType, T]):
    def __init__(
        self,
        *,
        population_size: int,
        generations: int,
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

    def _generate_individual(self, parents: Sequence[IndividualType]) -> IndividualType:
        individual = parents[random.randint(0, len(parents) - 1)]
        for m_op, probability in self.multiple_individual_operator:
            if random.random() < probability:
                individual = m_op(
                    [individual, parents[random.randint(0, len(parents) - 1)]]
                )
        for s_op, probability in self.single_individual_operator:
            if random.random() < probability:
                individual = s_op(individual)

        return individual

    def _should_stop(self):
        self.iterations += 1
        return self.iterations >= self.generations
