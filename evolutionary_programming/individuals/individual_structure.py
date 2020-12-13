from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable, Protocol, Callable

from typing_extensions import Final

from evolutionary_programming.genes.gene_definition import GeneDefinition


class InvalidIndividual(ValueError):
    pass


G = TypeVar("G", covariant=True)


class IndividualType(Protocol[G], Iterable[G]):
    ...


T = TypeVar("T")
Q = TypeVar("Q")


class IndividualStructure(Generic[G], ABC):
    """
    Defines the structure of a class of individuals (problem solutions) through its genes.

    :param  Callable[[Iterable[G]], IndividualType[G]] gene_holder: method to generate the concrete representation of an individual from an iterable
    """

    def __init__(self, gene_holder: Callable[[Iterable[G]], IndividualType[G]]):
        self._gene_holder: Final = gene_holder

    def __len__(self):
        """ Dimensions of the solution"""
        ...

    @abstractmethod
    def __getitem__(self, pos: int) -> GeneDefinition[G]:
        """ Returns gene identified by pos"""
        ...

    @abstractmethod
    def build(self) -> IndividualType[G]:
        """ Generates a specific individual of this class."""
        ...

    def build_individual_from_genes_values(self, it: Iterable[G]) -> IndividualType[G]:
        """Generates an individual starting from provided values

        Specifically, element in the iterable at position i will correspond to the value
        taken by the gene in position i.

        :param Iterable[G] it: iterable of values of the genes composing the individual to be built.
        """
        return self._gene_holder(it)
