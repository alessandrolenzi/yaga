from typing import TypeVar, Protocol, Sized, Iterable, runtime_checkable

GeneType = TypeVar("GeneType", covariant=True)
IndividualType = TypeVar("IndividualType")


class SequentialIndividualType(Protocol[GeneType], Sized, Iterable[GeneType]):
    pass

@runtime_checkable
class MultipleIndividualOperatorProtocol(Protocol[IndividualType]):
    def __call__(
        self, selected: IndividualType, it: Iterable[IndividualType]
    ) -> IndividualType:
        ...

@runtime_checkable
class SingleIndividualOperatorProtocol(Protocol[IndividualType]):
    def __call__(self, selected: IndividualType) -> IndividualType:
        pass
