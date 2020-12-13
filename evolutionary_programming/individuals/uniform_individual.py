from typing import TypeVar, Optional, Tuple, Final, Sequence, Union, Iterable, \
    Generic

from evolutionary_programming.evolutionary_algorithm import IndividualStructure
from evolutionary_programming.individuals.gene_definition import GeneDefinition

GenesType = TypeVar("GenesType")
SType = TypeVar("SType")

class UniformIndividualStructure(IndividualStructure[GenesType]):
    def __init__(self, genes: Union[Tuple[GeneDefinition[GenesType], ...], GeneDefinition[GenesType]]):
        self.genes: Final[Tuple[GeneDefinition[GenesType], ...]] = (genes, ) if isinstance(genes, GeneDefinition) else genes
        super().__init__(tuple)

    def define_gene(
        self, gene_definition: GeneDefinition[GenesType]
    ):
        our_gene = (gene_definition,)
        return self.__class__(self.genes + our_gene)

    def __getitem__(self, item: int):
        if 0 <= item < len(self.genes):
            return self.genes[item]
        raise ValueError(f"No gene with id {item}")

    def __len__(self):
        return len(self.genes)

    def build(self) -> Sequence[GenesType]:
        return tuple(gene.generate() for gene in self.genes)

    def build_individual_from_genes_values(self, it: Iterable[GenesType]) -> Sequence[GenesType]:
        return tuple(it)