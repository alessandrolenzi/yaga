from typing import TypeVar, Tuple, Union, Sequence
from yaga_ga.evolutionary_algorithm.genes import GeneDefinition
from .protocols import IterableIndividualStructure
from .traits.gene_sequence import GeneSequenceTrait
from .traits.linear_individual import LinearIndividualTrait

GenesType = TypeVar("GenesType")
SType = TypeVar("SType")


class UniformIndividualStructure(
    GeneSequenceTrait[GeneDefinition[GenesType]],
    LinearIndividualTrait[GenesType],
    IterableIndividualStructure[Tuple[GenesType, ...], GenesType],
):
    """
    Represents an individual with genes all of the same type.

    :param Sequence[GeneDefinition] or GeneDefinition genes: initial genes
    """

    def __init__(
        self,
        genes: Union[Sequence[GeneDefinition[GenesType]], GeneDefinition[GenesType]],
    ):
        GeneSequenceTrait.__init__(self, genes)
        LinearIndividualTrait.__init__(self, self.genes)

    def add_gene(self, gene_definition: GeneDefinition[GenesType]):
        return self.__class__(self._update_genes(gene_definition))
