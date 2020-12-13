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
from evolutionary_programming.individuals.traits.gene_sequence import \
    GeneSequenceTrait

GenesType = TypeVar("GenesType")
SType = TypeVar("SType")


class UniformIndividualStructure(GeneSequenceTrait[GeneDefinition[GenesType]], IndividualStructure[GenesType]):
    def __init__(
        self,
        genes: Union[Tuple[GeneDefinition[GenesType], ...], GeneDefinition[GenesType]],
        individual_class: Optional[
            Callable[[Iterable[GenesType]], IndividualType[GenesType]]
        ] = None,
    ):
        GeneSequenceTrait.__init__(self, genes)
        IndividualStructure.__init__(self, individual_class or tuple)

    def define_gene(self, gene_definition: GeneDefinition[GenesType]):
        return self.__class__(self._update_genes(gene_definition), individual_class=self._builder)

    def build(self) -> IndividualType[GenesType]:
        return self._builder(gene.generate() for gene in self.genes)

