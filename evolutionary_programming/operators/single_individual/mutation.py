import random
from typing import List, Tuple, Generic, TypeVar, cast, Iterable, Sequence

from typing_extensions import Final

from evolutionary_programming.genes import GeneDefinition
from evolutionary_programming.individuals import IndividualStructure
from evolutionary_programming.operators.protocols import SequentialIndividualType
from evolutionary_programming.operators.single_individual.base import (
    SingleIndividualOperator,
)
from evolutionary_programming.operators.base import InvalidOperatorError, GeneType
from evolutionary_programming.utils.random_selection import random_selection

T = TypeVar("T")


class MutationOperator(SingleIndividualOperator[SequentialIndividualType[T], T]):
    def __init__(
        self,
        individual_structure: IndividualStructure[SequentialIndividualType[T], T],
        genes_to_mutate: int = 1,
    ):
        super().__init__(individual_structure)
        if genes_to_mutate < 1:
            raise InvalidOperatorError(
                "Cannot have a mutation operator working on less than 1 gene per individual."
            )
        self.genes_to_mutate: Final = genes_to_mutate

    def __call__(
        self, _individual: SequentialIndividualType[T]
    ) -> SequentialIndividualType[T]:

        return self.individual_structure.build_individual_from_genes_values(
            self._new_individual_values(_individual)
        )

    def make_mutation(self, gene_definition: GeneDefinition[T], _value: T) -> T:
        return gene_definition.generate()

    def _new_individual_values(
        self, _individual: SequentialIndividualType[T]
    ) -> Iterable[T]:
        genes_to_mutate = {
            index: gene_def
            for index, gene_def in cast(
                Sequence[Tuple[int, GeneDefinition[T]]],
                random_selection(
                    enumerate(self.individual_structure), self.genes_to_mutate
                ),
            )
        }
        for gene_index, gene_value in enumerate(_individual):
            if gene_index in genes_to_mutate:
                yield genes_to_mutate[gene_index].generate()
            else:
                yield gene_value
