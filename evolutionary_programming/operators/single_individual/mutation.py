import random
from typing import List, Tuple, Generic, TypeVar, cast, Iterable

from typing_extensions import Final

from evolutionary_programming.genes import GeneDefinition
from evolutionary_programming.individuals import IndividualStructure
from evolutionary_programming.operators.protocols import IterableIndividualType
from evolutionary_programming.operators.single_individual.base import (
    SingleIndividualOperator,
)
from evolutionary_programming.operators.base import InvalidOperatorError, GeneType

T = TypeVar("T")


class MutationOperator(SingleIndividualOperator[IterableIndividualType[T], T]):
    def __init__(
        self,
        individual_structure: IndividualStructure[IterableIndividualType[T], T],
        genes_to_mutate: int = 1,
    ):
        super().__init__(individual_structure)
        if genes_to_mutate < 1:
            raise InvalidOperatorError(
                "Cannot have a mutation operator working on less than 1 gene per individual."
            )
        self.genes_to_mutate: Final = genes_to_mutate

    def __call__(
        self, _individual: IterableIndividualType[T]
    ) -> IterableIndividualType[T]:
        mutations: List[Tuple[int, T]] = []
        fenotype: List[T] = []
        for pos, (gene_definition, value) in enumerate(
            zip(self.individual_structure, _individual)
        ):
            if pos < self.genes_to_mutate:
                mutations.append((pos, value))
                fenotype.append(self.make_mutation(gene_definition, value))
                continue
            r = random.randint(0, pos)
            if r < self.genes_to_mutate:
                fenotype[mutations[r][0]] = mutations[r][1]
                mutations[r] = (pos, value)
                fenotype.append(self.make_mutation(gene_definition, value))
                continue
            fenotype.append(value)
        return self.individual_structure.build_individual_from_genes_values(fenotype)

    def make_mutation(self, gene_definition: GeneDefinition[T], _value: T) -> T:
        return gene_definition.generate()
