from typing import TypeVar, Protocol, Sized, Iterable

GeneType = TypeVar("GeneType", covariant=True)
IndividualType = TypeVar("IndividualType")


class SequentialIndividualType(Protocol[GeneType], Sized, Iterable[GeneType]):
    pass


class MultipleIndividualOperatorProtocol(Protocol[IndividualType]):
    def __call__(
        self, selected: IndividualType, it: Iterable[IndividualType]
    ) -> IndividualType:
        ...


class SingleIndividualOperatorProtocol(Protocol[IndividualType]):
    def __call__(self, selected: IndividualType) -> IndividualType:
        pass
