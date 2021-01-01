from abc import ABC, abstractmethod
from typing import (
    Generic,
    Sequence,
    Tuple,
    Iterable,
    Final,
    Protocol,
    TypeVar,
    Callable,
)

from evolutionary_programming.details import Comparable
from evolutionary_programming.individuals.individual_structure import IndividualType, G

T = TypeVar("T", bound=Comparable)


class Selector(Generic[G, T]):
    def __init__(self, selection_size: int):
        self.selection_size = selection_size

    @abstractmethod
    def __call__(
        self, population: Sequence[Tuple[IndividualType[G], T]]
    ) -> Iterable[IndividualType[G]]:
        ...
