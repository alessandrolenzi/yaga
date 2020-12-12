import random
from copy import copy
from typing import List, Tuple, Callable, Iterator, Iterable, Sequence, Optional
from typing_extensions import Final

from evolutionary_programming.selectors.selector import Selector

IType = List[bool]


class BinaryGeneticAlgorithm:
    genes: Final[int]
    population_size: Final[int]
    crossover_probability: Final[float]
    mutation_probability: Final[float]

    def __init__(
        self,
        *,
        genes: int,
        population_size: int,
        selector: Selector[IType],
        crossover_rate: float,
        mutation_rate: float,
        elite_ratio: float = 0,
    ):

        self.genes = genes
        self.population_size = population_size
        self.selector = selector
        self.crossover_probability = crossover_rate
        self.mutation_probability = mutation_rate
        self.population: List[IType] = []
        self.iterations = 0
        self.elite_size = int(elite_ratio * population_size)

    def initialize(self, initial_population: Optional[Sequence[IType]] = None):
        if initial_population:
            self.population = [i for i in initial_population]

        while len(self.population) < self.population_size:
            self.population.append(self._random_individual())
        return self

    def _random_individual(self) -> IType:
        individual = [False] * self.genes
        for position in range(self.genes):
            individual[position] = bool(random.randint(0, 1))
        return individual

    def run(self, evaluation_function: Callable[[IType], float]) -> Tuple[IType, float]:
        while not self._should_stop():
            evaluated_population = self._evaluate(evaluation_function)
            self.population = list(
                self._new_generation(zip(self.population, evaluated_population))
            )
        return next(zip(self.population, self._evaluate(evaluation_function)))

    def _new_generation(
        self, evaluated_population: Iterable[Tuple[IType, float]]
    ) -> Iterator[IType]:
        pop = list(evaluated_population)
        parents = list(self._select(pop))
        sorted_population = sorted(
            pop,
            key=lambda individual_score_tuple: individual_score_tuple[1],
            reverse=True,
        )
        print(f"best is {sorted_population[0][1]}")
        elites = [i[0] for i in sorted_population[: self.elite_size]]
        yield from elites
        for _ in range(self.population_size - self.elite_size):
            yield self._generate_individual(parents)

    def _generate_individual(self, parents: Sequence[IType]) -> IType:
        individual = parents[random.randint(0, len(parents) - 1)]
        if random.random() < self.crossover_probability:
            parent_2 = parents[random.randint(0, len(parents) - 1)]
            return self._crossover(individual, parent_2)

        if random.random() < self.mutation_probability:
            individual = self._mutate(individual)
        return individual

    def _crossover(self, individual_1: IType, individual_2: IType) -> IType:
        crossover_point = random.randint(0, self.genes - 1)
        return individual_1[:crossover_point] + individual_2[crossover_point:]

    def _mutate(self, _individual: IType):
        individual = copy(_individual)
        mutation_point = random.randint(0, self.genes - 1)
        individual[mutation_point] = bool((individual[mutation_point] + 1) % 2)
        return individual

    def _evaluate(
        self, evaluation_function: Callable[[IType], float]
    ) -> Iterator[float]:
        for individual in self.population:
            yield evaluation_function(individual)

    def _select(self, population: Sequence[Tuple[IType, float]]) -> Iterator[IType]:
        return self.selector(population)

    def _should_stop(self):
        self.iterations += 1
        print(f"Iteration: {self.iterations}")
        return self.iterations >= 3000
