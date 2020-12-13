import itertools
import random
from typing import Generic

from typing_extensions import Final

from evolutionary_programming.individuals.individual_structure import \
    IndividualStructure, G, IndividualType


class MultipleIndividualOperator(Generic[G]):
    def __init__(self, individual_structure: IndividualStructure[G]):
        self.individual_structure: Final = individual_structure


class OnePointCrossoverOperator(MultipleIndividualOperator[G]):


    def __call__(
        self, _parent1: IndividualType[G], _parent2: IndividualType[G]
    ) -> IndividualType:
        crossover_point = random.randint(0, len(self.individual_structure) - 1)
        serialised_individual = itertools.chain(
            itertools.islice(_parent1, crossover_point),
            itertools.islice(_parent2, crossover_point, None),
        )
        return self.individual_structure.build_individual_from_genes_values(
            serialised_individual
        )


