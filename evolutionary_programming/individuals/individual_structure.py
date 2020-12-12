from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Iterable

from evolutionary_programming.individuals.gene_definition import GeneDefinition
from evolutionary_programming.selectors.selector import IndividualType

T = TypeVar("T")
Q = TypeVar("Q")


class IndividualStructure(Generic[IndividualType], ABC):
    @abstractmethod
    def define_gene(self: T, gene_definition: GeneDefinition[Q]) -> T:
        ...

    def __len__(self):
        ...

    @abstractmethod
    def __getitem__(self, item: int) -> GeneDefinition[Q]:
        ...

    @abstractmethod
    def build(self) -> IndividualType:
        ...

    @abstractmethod
    def build_individual_from_genes_values(self, it: Iterable[Q]) -> IndividualType:
        ...
