from evolutionary_programming.builder import EvolutionaryAlgorithmBuilder
from evolutionary_programming.genes import IntGene
from evolutionary_programming.individuals.uniform_individual import (
    UniformIndividualStructure,
)


class Binary(EvolutionaryAlgorithmBuilder):
    def __init__(
        self,
        population_size: int,
        generations: int,
        solution_size: int,
    ):
        individual_structure = UniformIndividualStructure(
            tuple(IntGene(lower_bound=0, upper_bound=1) for _ in range(solution_size))
        )
        super().__init__(
            population_size, generations, individual_structure=individual_structure
        )
