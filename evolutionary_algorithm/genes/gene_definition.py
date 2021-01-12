from abc import ABC, abstractmethod
from typing import Generic, TypeVar

GeneType = TypeVar("GeneType")


class GeneDefinition(Generic[GeneType], ABC):
    """
    Represents a gene (a part of a solution).

    A GeneDefinition represents a certain feature of the problem. It emits a concrete solution with generate()
    """

    @abstractmethod
    def generate(self) -> GeneType:
        """Generates a specific piece of a solution (gene).
        :returns a gene instance.
        """
        pass
