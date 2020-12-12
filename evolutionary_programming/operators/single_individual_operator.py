import itertools
import random
from copy import copy
from typing import Generic, Iterable

from typing_extensions import Final

from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure,
)
from evolutionary_programming.selectors.selector import IndividualType


class SingleIndividualOperator(Generic[IndividualType]):
    pass


class MutationOperator(Generic[IndividualType]):
    def __init__(
        self,
        individual_structure: IndividualStructure[IndividualType],
        genes_to_mutate: int = 1,
    ):
        self.individual_structure: Final = individual_structure
        self.genes_to_mutate: Final = genes_to_mutate

    def __call__(self, _individual: IndividualType) -> IndividualType:
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


class MultipleIndividualOperator(Generic[IndividualType]):
    pass


class OnePointCrossoverOperator(Generic[IndividualType]):
    def __init__(self, individual_structure: IndividualStructure[IndividualType]):
        self.individual_structure: Final = individual_structure

    def __call__(
        self, _parent1: IndividualType, _parent2: IndividualType
    ) -> IndividualType:
        crossover_point = random.randint(0, len(self.individual_structure) - 1)
        serialised_individual = itertools.chain(
            itertools.islice(_parent1, crossover_point),
            itertools.islice(_parent2, crossover_point, None),
        )
        return self.individual_structure.build_individual_from_genes_values(
            serialised_individual
        )
