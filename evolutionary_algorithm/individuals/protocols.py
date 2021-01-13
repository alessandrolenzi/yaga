from typing import TYPE_CHECKING, Iterable, TypeVar

from evolutionary_algorithm.genes import GeneDefinition
from evolutionary_algorithm.individuals import IndividualStructure

T = TypeVar("T")
Q = TypeVar("Q")
if TYPE_CHECKING:

    class IterableIndividualStructure(
        IndividualStructure[Q, T], Iterable[GeneDefinition[T]]
    ):
        ...


else:
    IterableIndividualStructure = IndividualStructure
