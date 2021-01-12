from enum import Enum
from evolutionary_algorithm import selectors

class SelectorType(Enum):
    Tournament = selectors.Tournament
    Random = selectors.Random
    Ranking = selectors.Ranking
    StochasticUniversalSampling = selectors.StochasticUniversalSampling
