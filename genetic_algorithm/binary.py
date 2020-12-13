from typing import Optional

from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.individuals.gene_definition import IntGene
from evolutionary_programming.individuals.individual_structure import IndividualType
from evolutionary_programming.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_programming.selectors.selector import Selector
from evolutionary_programming.selectors.stochastic_universal_sampling import (
    StochasticUniversalSampling,
)


class Binary(EvolutionaryAlgorithm):
    def __init__(
        self,
        *,
        genes: int,
        population_size: int,
        generations: int,
        selection_probability: float = 0.5,
        elite_ratio: float = 0.0,
        crossover_probability: float = 0.5,
        mutation_probability: float = 0.1,
        selector: Optional[Selector[IndividualType[int]]] = None
    ):
        super().__init__(
            population_size,
            generations,
            elite_ratio,
            crossover_probability,
            mutation_probability,
        )
        self.define_individual_structure(
            UniformIndividualStructure(
                tuple(IntGene(lower_bound=0, upper_bound=1) for _ in range(genes))
            )
        )
        self.define_selector(
            selector
            or StochasticUniversalSampling(
                int(self.population_size * selection_probability)
            )
        )
