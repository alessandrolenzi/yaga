import itertools
import random
from typing import Generic

from typing_extensions import Final

from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure,
    IndividualType,
    G,
)


class SingleIndividualOperator(Generic[G]):
    def __init__(self, individual_structure: IndividualStructure[G]):
        self.individual_structure: Final = individual_structure


class InvalidOperatorError(ValueError):
    pass


class MutationOperator(SingleIndividualOperator[G]):
    def __init__(
        self, individual_structure: IndividualStructure[G], genes_to_mutate: int = 1
    ):
        super().__init__(individual_structure)
        if genes_to_mutate < 1:
            raise InvalidOperatorError(
                "Cannot have a mutation operator working on less than 1 gene per individual."
            )
        self.genes_to_mutate: Final = genes_to_mutate

    def __call__(self, _individual: IndividualType[G]) -> IndividualType[G]:
        individual = self._apply_mutation(self.individual_structure, _individual)
        for _ in range(self.genes_to_mutate - 1):
            individual = self._apply_mutation(self.individual_structure, individual)
        return individual

    @classmethod
    def _apply_mutation(
        cls, individual_structure: IndividualStructure[G], individual: IndividualType[G]
    ) -> IndividualType[G]:
        mutation_point = random.randint(0, len(individual_structure) - 1)
        return individual_structure.build_individual_from_genes_values(
            itertools.chain(
                itertools.islice(individual, mutation_point),
                [individual_structure[mutation_point].generate()],
                itertools.islice(individual, mutation_point + 1, None),
            )
        )
