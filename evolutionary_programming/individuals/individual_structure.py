from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable, Iterator, Protocol


class InvalidIndividual(ValueError):
    pass


IndividualType = TypeVar("IndividualType", covariant=True)
GeneType = TypeVar("GeneType", contravariant=True)


class IndividualStructure(Protocol[IndividualType, GeneType]):
    """
    Defines a class of individuals (problem solutions) through genes.
    """

    def build(self) -> IndividualType:
        """ Generates an instance of this class."""
        pass

    def build_individual_from_genes_values(
        self, it: Iterable[GeneType]
    ) -> IndividualType:
        """Generates an individual starting from provided values

        Specifically, element in the iterable at position i will correspond to the value
        taken by the gene in position i.

        :param Iterable[G] it: iterable of values of the genes composing the individual to be built.
        """
        pass
