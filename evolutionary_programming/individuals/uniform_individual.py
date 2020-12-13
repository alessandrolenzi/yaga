from typing import (
    TypeVar,
    Optional,
    Tuple,
    Final,
    Sequence,
    Union,
    Iterable,
    Generic,
    Type,
    Callable,
)

from evolutionary_programming.evolutionary_algorithm import IndividualStructure
from evolutionary_programming.individuals.gene_definition import GeneDefinition
from evolutionary_programming.individuals.individual_structure import (
    IndividualType,
    InvalidIndividual,
)

GenesType = TypeVar("GenesType")
SType = TypeVar("SType")


class UniformIndividualStructure(IndividualStructure[GenesType]):
    def __init__(
        self,
        genes: Union[Tuple[GeneDefinition[GenesType], ...], GeneDefinition[GenesType]],
        individual_class: Optional[
            Callable[[Iterable[GenesType]], IndividualType[GenesType]]
        ] = None,
    ):
        self.genes: Final[Tuple[GeneDefinition[GenesType], ...]] = (
            (genes,) if isinstance(genes, GeneDefinition) else genes
        )
        super().__init__(individual_class or tuple)

    def define_gene(self, gene_definition: GeneDefinition[GenesType]):
        our_gene = (gene_definition,)
        return self.__class__(self.genes + our_gene, individual_class=self._builder)

    def __getitem__(self, item: int):
        if 0 <= item < len(self.genes):
            return self.genes[item]
        raise IndexError(f"No gene with id {item}")

    def __len__(self):
        return len(self.genes)

    def build(self) -> IndividualType[GenesType]:
        return self._builder(gene.generate() for gene in self.genes)

    def build_individual_from_genes_values(
        self, it: Iterable[GenesType]
    ) -> IndividualType[GenesType]:
        return self._builder(it)
