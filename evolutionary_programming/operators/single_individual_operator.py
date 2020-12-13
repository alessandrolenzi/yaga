import itertools
import random
from copy import copy
from typing import Generic

from typing_extensions import Final

from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure, IndividualType, G,
)


class SingleIndividualOperator(Generic[G]):
    def __init__(self, individual_structure: IndividualStructure[G]):
        self.individual_structure: Final = individual_structure



class MutationOperator(SingleIndividualOperator[G]):
    def __init__(self,
                 individual_structure: IndividualStructure[G],
                 genes_to_mutate: int = 1):
        super().__init__(individual_structure)
        self.genes_to_mutate: Final = genes_to_mutate

    def __call__(self, _individual: IndividualType[G]) -> IndividualType[G]:
        individual = copy(_individual)
        for _ in range(self.genes_to_mutate):
            mutation_point = random.randint(0, len(self.individual_structure) - 1)
            individual = self.individual_structure.build_individual_from_genes_values(
                itertools.chain(
                    itertools.islice(_individual, mutation_point),
                    [self.individual_structure[mutation_point].generate()],
                    itertools.islice(_individual, mutation_point + 1, None),
                )
            )
        return individual


