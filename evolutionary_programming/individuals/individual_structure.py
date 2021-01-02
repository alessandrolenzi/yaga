from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable, Iterator

from evolutionary_programming.genes.gene_definition import GeneDefinition


class InvalidIndividual(ValueError):
    pass


IndividualType = TypeVar("IndividualType")
GeneType = TypeVar("GeneType")


class IndividualStructure(Generic[IndividualType, GeneType], ABC):
    """
    Defines the structure of a class of individuals (problem solutions) through its genes.
    """

    @abstractmethod
    def build(self) -> IndividualType:
        """ Generates a specific individual of this class."""
        pass

    @abstractmethod
    def build_individual_from_genes_values(
        self, it: Iterable[GeneType]
    ) -> IndividualType:
        """Generates an individual starting from provided values

        Specifically, element in the iterable at position i will correspond to the value
        taken by the gene in position i.

        :param Iterable[G] it: iterable of values of the genes composing the individual to be built.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[GeneDefinition[GeneType]]:
        ...
