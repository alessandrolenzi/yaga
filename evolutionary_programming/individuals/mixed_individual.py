from typing import TypeVar, Any, Sequence, Union, Tuple, Optional, Callable, Iterable
from typing_extensions import Final
from evolutionary_programming.individuals.gene_definition import GeneDefinition
from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure,
    IndividualType,
)

T = TypeVar("T")
Q = TypeVar("Q")


class MixedIndividualStructure(IndividualStructure[Any]):
    def __init__(
        self,
        genes: Union[Tuple[GeneDefinition, ...], GeneDefinition[T]],
        individual_class: Optional[Callable[[Iterable[T]], IndividualType[Any]]] = None,
    ):

        self.genes: Final[Tuple[GeneDefinition[T], ...]] = (
            (genes,) if isinstance(genes, GeneDefinition) else genes
        )
        super().__init__(individual_class or tuple)

    def define_gene(self, gene_definition: GeneDefinition[Q]):
        return self.__class__(
            self.genes + (gene_definition,), individual_class=self._builder
        )

    def __len__(self):
        return len(self.genes)

    def __getitem__(self, item: int) -> GeneDefinition:
        return self.genes[item]

    def build(self):
        return self._builder(i.generate() for i in self.genes)

    def build_individual_from_genes_values(self, ind):
        return self._builder(ind)
