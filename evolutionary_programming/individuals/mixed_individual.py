from typing import TypeVar, Any, Sequence

from evolutionary_programming.individuals.gene_definition import GeneDefinition
from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure,
)

T = TypeVar("T")
Q = TypeVar("Q")


class MixedIndividualStructure(IndividualStructure[Sequence[Any]]):
    def __init__(self, gene: GeneDefinition[T]):
        self.genes = [gene]

    def define_gene(self, gene_definition: GeneDefinition[Q]):
        self.genes.append(gene_definition)
        return self

    def __len__(self):
        return len(self.genes)

    def __getitem__(self, item: int) -> GeneDefinition:
        return self.genes[item]

    def build(self):
        return tuple(i.generate() for i in self.genes)

    def build_individual_from_genes_values(self, ind):
        return tuple(ind)
