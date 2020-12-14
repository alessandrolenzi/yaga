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
    :param genes_holder: callable returning a structure responsible of holding concrete genes (default is tuple)
    """
    def __init__(
        self,
        genes: Union[Sequence[GeneDefinition[GenesType]], GeneDefinition[GenesType]],
        genes_holder: Optional[
            Callable[[Iterable[GenesType]], IndividualType[GenesType]]
        ] = None,
    ):
        GeneSequenceTrait.__init__(self, genes)
        IndividualStructure.__init__(self, genes_holder or tuple)

    def add_gene(self, gene_definition: GeneDefinition[GenesType]):
        return self.__class__(
            self._update_genes(gene_definition), genes_holder=self._gene_holder
        )
