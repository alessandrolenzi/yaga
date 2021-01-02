from typing import TypeVar, Protocol, Iterable, Generic

GeneType = TypeVar("GeneType", covariant=True)


class IterableIndividualType(Protocol[GeneType], Iterable[GeneType]):
    pass
