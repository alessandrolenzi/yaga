from typing import TypeVar, Callable, Tuple

from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.details import Comparable
from evolutionary_algorithm.genes import IntGene
from evolutionary_algorithm.individuals import IndividualStructure
from evolutionary_algorithm.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.protocols import (
    MultipleIndividualOperatorProtocol,
)
from evolutionary_algorithm.operators.single_individual.mutation import MutationOperator

from evolutionary_algorithm.selectors import Selector

ScoreType = TypeVar("ScoreType", bound=Comparable)


class Binary(EvolutionaryAlgorithmBuilder[Tuple[int, ...], int]):
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
        individual_structure = UniformIndividualStructure(
            tuple(IntGene(lower_bound=0, upper_bound=1) for _ in range(solution_size))
        )

        super().__init__(
            population_size,
            generations,
            individual_structure=individual_structure,
            elite_size=elite_size,
        )
        self.add_operator_instance(
            crossover(individual_structure), crossover_probability
        )
        self.add_operator_instance(
            MutationOperator(individual_structure), mutation_probability
        )
        self.selector(selector)
