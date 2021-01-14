from typing import Callable, Tuple

from yaga_ga.evolutionary_algorithm.individuals import IndividualStructure
from yaga_ga.evolutionary_algorithm.operators.protocols import (
    MultipleIndividualOperatorProtocol,
)
from yaga_ga.evolutionary_algorithm.selectors import Selector
from yaga_ga.genetic_algorithm.integer_ga import IntegerGeneticAlgorithm


class BinaryGeneticAlgorithm(IntegerGeneticAlgorithm):
    def __init__(
        self,
        population_size: int,
        generations: int,
        solution_size: int,
        crossover: Callable[
            [IndividualStructure[Tuple[int, ...], int]],
            MultipleIndividualOperatorProtocol[Tuple[int, ...]],
        ],
        selector: Selector,
        crossover_probability: float,
        mutation_probability: float,
        elite_size: int = 0,
    ):
        super().__init__(
            population_size,
            generations,
            solution_size,
            crossover,
            selector,
            crossover_probability,
            mutation_probability,
            lower_bound=0,
            upper_bound=1,
            elite_size=elite_size,
        )
