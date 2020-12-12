from typing import Sequence

from evolutionary_programming.selectors.random import Random
from evolutionary_programming.selectors.ranking import Ranking
from evolutionary_programming.selectors.stochastic_universal_sampling import (
    StochasticUniversalSampling,
)
from evolutionary_programming.selectors.tournament import Tournament
from genetic_algorithm.binary import BinaryGeneticAlgorithm


def evaluate_ones(ind: Sequence[bool]):
    return abs(11 * sum(i for i in ind) - 150)


def all_ones():
    algo = BinaryGeneticAlgorithm(
        genes=30,
        population_size=100,
        selector=Tournament(tournament_size=2, selection_size=20),
        crossover_rate=0.8,
        mutation_rate=0.5,
        elite_ratio=0.04,
    )
    algo.initialize()
    print(algo.run(evaluation_function=evaluate_ones))


if __name__ == "__main__":
    all_ones()
