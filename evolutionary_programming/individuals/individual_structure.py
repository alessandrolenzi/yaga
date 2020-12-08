from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from evolutionary_programming.individuals.gene_factory import GeneDefinition
from evolutionary_programming.selectors.selector import IndividualType

T = TypeVar('T')
class IndividualStructure(Generic[IndividualType], ABC):
    def __init__(self):
        self.frozen = False

    @abstractmethod
    def define_gene(self: Type[T], gene_definition: GeneDefinition) -> "T":
        ...

    def __len__(self):
        ...

    @abstractmethod
    def __getattr__(self, item: int):
        ...

    def freeze(self):
        self.frozen = True

    @abstractmethod
    def build(self) -> IndividualType:
       ...