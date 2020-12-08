from typing import Generic, TypeVar, Optional, Tuple, Final, Sequence

from evolutionary_programming.evolutionary_algorithm import IndividualStructure
from evolutionary_programming.individuals.gene_factory import GeneDefinition

GenesType = TypeVar('GenesType')

class UniformIndividualStructure(IndividualStructure[Sequence[GenesType]]):

    def __init__(self, genes: Optional[Tuple[GeneDefinition[GenesType], ...]] = None):
        self.genes: Final = genes or tuple()
        self.frozen = False
        super().__init__()

    def define_gene(self, gene_definition: GeneDefinition[GenesType]) -> "UniformIndividualStructure[GenesType]":
        if self.frozen:
            raise ValueError('Cannot add gene definitions to a frozen individual structure')
        our_gene = gene_definition,
        return UniformIndividualStructure(
            self.genes + our_gene
        )

    def __getattr__(self, item: int):
        if 0 <= item < len(self.genes):
            return self.genes[item]
        raise ValueError(f'No gene with id {item}')

    def __len__(self):
        return len(self.genes)

    def freeze(self):
        self.frozen = True

    def build(self) -> Sequence[GenesType]:
        return tuple(gene.generate() for gene in self.genes)