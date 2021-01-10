from typing import TypeVar, Protocol, Sized, Iterable

from evolutionary_programming.individuals import IndividualType

GeneType = TypeVar("GeneType", covariant=True)


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
