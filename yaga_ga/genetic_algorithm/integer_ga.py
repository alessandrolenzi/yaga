from typing import Tuple, Callable

from yaga_ga.evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from yaga_ga.evolutionary_algorithm.genes import IntGene
from yaga_ga.evolutionary_algorithm.individuals import (
    IndividualStructure,
    UniformIndividualStructure,
)
from yaga_ga.evolutionary_algorithm.operators.protocols import (
    MultipleIndividualOperatorProtocol,
)
from yaga_ga.evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)
from yaga_ga.evolutionary_algorithm.selectors import Selector


class IntegerGeneticAlgorithm(EvolutionaryAlgorithmBuilder[Tuple[int, ...], int]):
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
        lower_bound: int,
        upper_bound: int,
        elite_size: int = 0,
    ):
        individual_structure = UniformIndividualStructure(
            tuple(
                IntGene(lower_bound=lower_bound, upper_bound=upper_bound)
                for _ in range(solution_size)
            )
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
