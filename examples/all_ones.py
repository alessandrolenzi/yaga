from typing import Sequence

from genetic_algorithm.binary import Binary as BinaryGeneticAlgorithm
from evolutionary_programming.selectors.tournament import Tournament


def evaluate_ones(ind: Sequence[bool]):
    return abs(11 * sum(i for i in ind) - 150)


def all_ones():
    algo = BinaryGeneticAlgorithm(
        genes=30,
        population_size=100,
        selector=Tournament(tournament_size=2, selection_size=20),
        crossover_probability=0.8,
        mutation_probability=0.5,
        elite_ratio=0.04,
        generations=100,
    )
    algo.initialize()
    print(algo.run(evaluation_function=evaluate_ones))


if __name__ == "__main__":
    all_ones()
