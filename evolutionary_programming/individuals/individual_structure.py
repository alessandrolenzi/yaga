from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable, Protocol, Type, Callable

from evolutionary_programming.individuals.gene_definition import GeneDefinition


class InvalidIndividual(ValueError):
    pass


G = TypeVar("G", covariant=True)


class IndividualType(Protocol[G], Iterable[G]):
    ...


T = TypeVar("T")
Q = TypeVar("Q")


class IndividualStructure(Generic[G], ABC):
    def __init__(self, individual_class: Callable[[Iterable[G]], IndividualType[G]]):
        self._builder = individual_class

    @abstractmethod
    def define_gene(self: T, gene_definition: GeneDefinition[G]) -> T:
        ...

    def __len__(self):
        ...

    @abstractmethod
    def __getitem__(self, item: int) -> GeneDefinition[G]:
        ...

    @abstractmethod
    def build(self) -> IndividualType[G]:
        ...

    @abstractmethod
    def build_individual_from_genes_values(self, it: Iterable) -> IndividualType[G]:
        ...
