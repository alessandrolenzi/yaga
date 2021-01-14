from typing import TYPE_CHECKING, Iterable, TypeVar

from yaga_ga.evolutionary_algorithm.genes import GeneDefinition
from yaga_ga.evolutionary_algorithm.individuals import IndividualStructure

T = TypeVar("T")
Q = TypeVar("Q")
if TYPE_CHECKING:

    class IterableIndividualStructure(
        IndividualStructure[Q, T], Iterable[GeneDefinition[T]]
    ):
        ...


else:
    IterableIndividualStructure = IndividualStructure
