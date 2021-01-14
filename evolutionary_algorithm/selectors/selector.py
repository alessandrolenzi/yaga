from typing import (
    Sequence,
    Tuple,
    Iterable,
    TypeVar,
)
from typing_extensions import Protocol

from evolutionary_algorithm.details import Comparable

T = TypeVar("T", bound=Comparable, contravariant=True)
IndividualType = TypeVar("IndividualType")


class Selector(Protocol[IndividualType, T]):
    selection_size: int

    def __call__(
        self, population: Sequence[Tuple[IndividualType, T]]
    ) -> Iterable[IndividualType]:
        ...
