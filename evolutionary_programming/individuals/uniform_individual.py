from typing import (
    TypeVar,
    Optional,
    Tuple,
    Union,
    Iterable,
    Callable,
)
from evolutionary_programming.genes.gene_definition import GeneDefinition
from .individual_structure import IndividualType, IndividualStructure
from .traits.gene_sequence import GeneSequenceTrait

GenesType = TypeVar("GenesType")
SType = TypeVar("SType")


class UniformIndividualStructure(
    GeneSequenceTrait[GeneDefinition[GenesType]], IndividualStructure[GenesType]
):
    def __init__(
        self,
        genes: Union[Tuple[GeneDefinition[GenesType], ...], GeneDefinition[GenesType]],
        individual_class: Optional[
            Callable[[Iterable[GenesType]], IndividualType[GenesType]]
        ] = None,
    ):
        GeneSequenceTrait.__init__(self, genes)
        IndividualStructure.__init__(self, individual_class or tuple)

    def add_gene(self, gene_definition: GeneDefinition[GenesType]):
        return self.__class__(
            self._update_genes(gene_definition), individual_class=self._builder
        )

    def build(self) -> IndividualType[GenesType]:
        return self._builder(gene.generate() for gene in self.genes)
