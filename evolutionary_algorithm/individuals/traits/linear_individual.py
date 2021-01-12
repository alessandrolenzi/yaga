from typing import TypeVar, Generic, Iterable, Tuple, Sequence

from evolutionary_algorithm.genes import GeneDefinition

T = TypeVar("T")


class LinearIndividualTrait(Generic[T]):
    genes_iterable: Sequence[GeneDefinition[T]]

    def __init__(self, genes: Sequence[GeneDefinition[T]]):
        self.genes_iterable = genes

    def build(self) -> Tuple[T, ...]:
        return tuple(i.generate() for i in self.genes_iterable)

    def build_individual_from_genes_values(self, it: Iterable[T]) -> Tuple[T, ...]:
        return tuple(i for i in it)
