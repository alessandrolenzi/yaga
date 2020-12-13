from typing import TypeVar, Any, Union, Tuple, Optional, Callable, Iterable
from typing_extensions import Final
from evolutionary_programming.individuals.gene_definition import GeneDefinition
from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure,
    IndividualType,
)
from evolutionary_programming.individuals.traits.gene_sequence import \
    GeneSequenceTrait
from evolutionary_programming.individuals.uniform_individual import GenesType

T = TypeVar("T")
Q = TypeVar("Q")


class MixedIndividualStructure(GeneSequenceTrait[GeneDefinition[Any]], IndividualStructure[Any]):
    def __init__(
        self,
        genes: Union[Tuple[GeneDefinition, ...], GeneDefinition[T]],
        individual_class: Optional[Callable[[Iterable[T]], IndividualType[Any]]] = None,
    ):
        GeneSequenceTrait.__init__(self, genes)
        IndividualStructure.__init__(self, individual_class or tuple)

    def define_gene(self, gene_definition: GeneDefinition[Q]):
        return self.__class__(
            self._update_genes(gene_definition), individual_class=self._builder
        )

    def build(self):
        return self._builder(i.generate() for i in self.genes)

    def build_individual_from_genes_values(self, ind):
        return self._builder(ind)
