from typing import Sequence

from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)
from evolutionary_algorithm.selectors.stochastic_universal_sampling import (
    StochasticUniversalSampling,
)

from genetic_algorithm.binary import Binary as BinaryGeneticAlgorithm


def evaluate_ones(ind: Sequence[bool]):
    return abs(11 * sum(i for i in ind) - 150)


def all_ones():
    algo = (
        BinaryGeneticAlgorithm(
            solution_size=30,
            population_size=100,
            generations=800,
        )
        .add_operator(MutationOperator, 0.01)
        .add_operator(OnePointCrossoverOperator, 0.8)
        .selector(StochasticUniversalSampling(selection_size=20))
        .initialize(evaluate_ones)
    )

    algo.run()


if __name__ == "__main__":
    all_ones()
