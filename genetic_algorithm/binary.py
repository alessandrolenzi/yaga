from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.genes import IntGene
from evolutionary_algorithm.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_algorithm.operators.protocols import \
    MultipleIndividualOperatorProtocol
from evolutionary_algorithm.operators.single_individual.mutation import \
    MutationOperator
from genetic_algorithm.crossover_types import CrossoverType

from evolutionary_algorithm.selectors import Selector
from genetic_algorithm.selector_type import SelectorType


class Binary(EvolutionaryAlgorithmBuilder):
    def __init__(
        self,
        population_size: int,
        generations: int,
        solution_size: int,
        crossover: MultipleIndividualOperatorProtocol[UniformIndividualStructure[int]],
        selector: Selector[UniformIndividualStructure[int]],
        crossover_probability: float,
        mutation_probability: float,
        elite_size: int
    ):
        individual_structure = UniformIndividualStructure(
            tuple(IntGene(lower_bound=0, upper_bound=1) for _ in range(solution_size))
        )
        super().__init__(
            population_size, generations, individual_structure=individual_structure,
            elite_size=elite_size
        )
        # self.add_operator(crossover_type.value, crossover_probability)
        self.add_operator(MutationOperator, mutation_probability)
        self.selector(selector)
