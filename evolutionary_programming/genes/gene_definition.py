from abc import ABC, abstractmethod
from typing import Generic, TypeVar

GeneType = TypeVar("GeneType")


class GeneDefinition(Generic[GeneType], ABC):
    """
    Represents a gene (a part of a solution).

    A GeneDefinition represents a certain feature of the problem
    we are trying to represent. It emits a concrete gene with generate()
    """

    @abstractmethod
    def generate(self) -> GeneType:
        """Generates a gene.
        :returns a gene instance.
        """
        pass
