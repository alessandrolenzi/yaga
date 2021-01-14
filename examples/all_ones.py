from typing import Sequence

from yaga_ga.evolutionary_algorithm.operators.multiple_individuals.crossover.two_points import (
    TwoPointsCrossoverOperator,
)
from yaga_ga.evolutionary_algorithm.selectors import (
    StochasticUniversalSampling,
)
from yaga_ga.genetic_algorithm import BinaryGeneticAlgorithm as BinaryGeneticAlgorithm


def evaluate_ones(ind: Sequence[int]):
    return sum(i for i in ind)


def all_ones():
    algo = (
        BinaryGeneticAlgorithm(
            solution_size=30,
            population_size=100,
            generations=800,
            crossover=TwoPointsCrossoverOperator,
            crossover_probability=0.8,
            mutation_probability=0.1,
            selector=StochasticUniversalSampling(selection_size=30),
        )
        .add_callback(lambda evolution: print(evolution.fittest))
        .initialize(evaluate_ones)
    )

    evolution = algo.run()
    print(f"Found solution {evolution.fittest} with score {evolution.fittest_score}")


if __name__ == "__main__":
    all_ones()
