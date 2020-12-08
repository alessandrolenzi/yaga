import random
from copy import copy
from typing import TypeVar, Optional, Sequence, Callable, Tuple, Iterator, \
    Iterable

from typing_extensions import Final

from evolutionary_programming.individuals.individual_structure import \
    IndividualStructure
from evolutionary_programming.operators.single_individual_operator import \
    MutationOperator, OnePointCrossoverOperator
from evolutionary_programming.selectors.selector import Selector
from genetic_algorithm.binary import IType

class EvolutionaryAlgorithm:
    population_size: Final[int]
    generations: Final[int]

    def __init__(self, population_size: int, generations: int, elite_ratio: float = 0.0, crossover_probability: float = 0.5, mutation_probability: float = 0.1):
        self.population_size = population_size
        self.generations = generations
        self.population: Sequence[Sequence[IType]] = []
        self.elite_size = int(elite_ratio * self.population_size)
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.iterations = 0

    def define_individual_structure(self, individual_structure: IndividualStructure[Sequence[IType]]):
        self.individual_structure = individual_structure
        return self

    def selector(self, selector: Selector[Sequence[IType]]):
        self.selector = selector
        return self

    def initialize(self, initial_population: Optional[Sequence[IType]] = None):
        if initial_population:
            self.population = [i for i in initial_population]

        while len(self.population) < self.population_size:
            self.population.append(self.individual_structure.build())
        return self


    def run(self, evaluation_function: Callable[[Sequence[IType]], float]) -> Tuple[IType, float]:
        while not self._should_stop():
            evaluated_population = self._evaluate(evaluation_function)
            self.population = list(self._new_generation(zip(self.population, evaluated_population)))
        return next(zip(self.population, self._evaluate(evaluation_function)))

    def _new_generation(self, evaluated_population: Iterable[Tuple[Sequence[IType], float]]) -> Iterator[Sequence[IType]]:
        pop = list(evaluated_population)
        parents = list(self._select(pop))
        sorted_population = sorted(pop,
               key=lambda individual_score_tuple: individual_score_tuple[1],
               reverse=True)
        print(f'best is {sorted_population[0]}')
        elites = [i[0] for i in sorted_population[:self.elite_size]]
        yield from elites
        for _ in range(self.population_size - self.elite_size):
            yield self._generate_individual(parents)


    def _generate_individual(self, parents: Sequence[Sequence[IType]]) -> IType:
        individual = parents[random.randint(0, len(parents)-1)]
        if random.random() < self.crossover_probability:
            parent_2 = parents[random.randint(0, len(parents)-1)]
            return self._crossover(individual, parent_2)

        if random.random() < self.mutation_probability:
            individual = self._mutate(individual)
        return individual

    def _crossover(self, individual_1: Sequence[IType], individual_2: Sequence[IType]) -> IType:
        return OnePointCrossoverOperator(self.individual_structure)(individual_1, individual_2)

    def _mutate(self, _individual: IType):
        return MutationOperator(self.individual_structure)(_individual)

    def _evaluate(self, evaluation_function: Callable[[Sequence[IType]], float]) -> Iterator[float]:
        for individual in self.population:
            yield evaluation_function(individual)

    def _select(self, population: Sequence[Tuple[Sequence[IType], float]]) -> Iterator[Sequence[IType]]:
        return self.selector(population)


    def _should_stop(self):
        self.iterations += 1
        print(f'Iteration: {self.iterations}')
        return self.iterations >= self.generations