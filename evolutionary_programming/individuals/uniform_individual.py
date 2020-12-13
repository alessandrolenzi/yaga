from typing import (
    TypeVar,
    Optional,
    Tuple,
    Union,
    Iterable,
    Callable,
    Sequence
)
from evolutionary_programming.genes.gene_definition import GeneDefinition
from .individual_structure import IndividualType, IndividualStructure
from .traits.gene_sequence import GeneSequenceTrait

GenesType = TypeVar("GenesType")
SType = TypeVar("SType")


class UniformIndividualStructure(
    GeneSequenceTrait[GeneDefinition[GenesType]], IndividualStructure[GenesType]
):
    """
    Represents an individual with genes all of the same type.

    :param Seuence[GeneDefinition] or GeneDefinition genes: initial genes
    :param
    """
    def __init__(
        self,
        genes: Union[Sequence[GeneDefinition[GenesType]], GeneDefinition[GenesType]],
        gene_holder: Optional[
            Callable[[Iterable[GenesType]], IndividualType[GenesType]]
        ] = None,
    ):
        GeneSequenceTrait.__init__(self, genes)
        IndividualStructure.__init__(self, gene_holder or tuple)

    def add_gene(self, gene_definition: GeneDefinition[GenesType]):
        return self.__class__(
            self._update_genes(gene_definition), gene_holder=self._gene_holder
        )

    def build(self) -> IndividualType[GenesType]:
        return self._gene_holder(gene.generate() for gene in self.genes)
