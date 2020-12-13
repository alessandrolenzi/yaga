from typing import TypeVar, Any, Union, Tuple, Optional, Callable, Iterable, Sequence
from evolutionary_programming.genes.gene_definition import GeneDefinition
from .individual_structure import (
    IndividualStructure,
    IndividualType,
)
from .traits.gene_sequence import GeneSequenceTrait

T = TypeVar("T")
Q = TypeVar("Q")


class MixedIndividualStructure(
    GeneSequenceTrait[GeneDefinition[Any]], IndividualStructure[Any]
):
    """Represents an individual structure with genes of different types"""

    def __init__(
        self,
        genes: Union[Sequence[GeneDefinition], GeneDefinition],
        gene_holder: Optional[
            Callable[[Iterable[Any]], IndividualType[Any]]
        ] = None,
    ):
        GeneSequenceTrait.__init__(self, genes)
        IndividualStructure.__init__(self, gene_holder or tuple)

    def add_gene(self, gene_definition: GeneDefinition[Q]):
        return self.__class__(
            self._update_genes(gene_definition), gene_holder=self._gene_holder
        )

    def build(self):
        return self._gene_holder(i.generate() for i in self.genes)

    def build_individual_from_genes_values(self, ind):
        return self._gene_holder(ind)
