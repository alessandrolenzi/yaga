from typing import TypeVar, Sequence, Final, Iterable, NamedTuple, Generic, \
    Callable

from evolutionary_programming.selectors.selector import IndividualType

IndividualRepresentationType = TypeVar('IndividualRepresentationType')

class PopulationPool(Generic[IndividualRepresentationType]):
    population: Final[Sequence[IndividualRepresentationType]]

    def __init__(self, individuals: Iterable[IndividualRepresentationType]):
        self.population = list(individuals)


class RankedIndividual(NamedTuple, Generic[IndividualType]):
    individual: IndividualType
    score: float

class RankedPopulationPool(PopulationPool[RankedIndividual[IndividualType]]):
    def __init__(self, ranker: Ranker[IndividualType], individuals: Iterable[IndividualType])
        super().__init__()
