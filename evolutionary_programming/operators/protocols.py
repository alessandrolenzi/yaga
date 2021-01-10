from typing import TypeVar, Protocol, Sized, Iterable

GeneType = TypeVar("GeneType", covariant=True)


class SequentialIndividualType(Protocol[GeneType], Sized, Iterable[GeneType]):
    pass
