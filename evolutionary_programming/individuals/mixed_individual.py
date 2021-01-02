from typing import TypeVar, Any, Union, Tuple, Optional, Callable, Iterable, Sequence
from evolutionary_programming.genes.gene_definition import GeneDefinition
from .individual_structure import (
    IndividualStructure,
)
from .traits.gene_sequence import GeneSequenceTrait
from .traits.linear_individual import LinearIndividualTrait

T = TypeVar("T")
Q = TypeVar("Q")


class MixedIndividualStructure(
    GeneSequenceTrait[GeneDefinition[Any]],
    LinearIndividualTrait[Any],
    IndividualStructure[Tuple, Any],
):
    """
    Represents an individual structure with genes of different types

    :param Seuence[GeneDefinition] or GeneDefinition genes: initial genes
    :param genes_holder: callable returning a structure responsible of holding concrete genes (default is tuple)
    """

    def __init__(
        self,
        genes: Union[Sequence[GeneDefinition], GeneDefinition],
    ):
        GeneSequenceTrait.__init__(self, genes)
        LinearIndividualTrait.__init__(self, self.genes)

    def add_gene(self, gene_definition: GeneDefinition[Q]):
        return self.__class__(self._update_genes(gene_definition))
