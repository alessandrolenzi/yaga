from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence, Tuple, Iterable, Final

IndividualType = TypeVar('IndividualType')

class Selector(Generic[IndividualType], ABC):
    """ Abstract Selector class.
    A Selector has the responsibility of selecting the elements of the population
    that can reproduce.
    Expects to receive an already scored population.
    :param selection_size (int) the number of surviving members of the population
    """
    selection_size: Final[int]
    def __init__(self, selection_size: int):
        self.selection_size = selection_size

    @abstractmethod
    def __call__(self, population: Sequence[Tuple[IndividualType, float]]) -> Iterable[IndividualType]:
        ...