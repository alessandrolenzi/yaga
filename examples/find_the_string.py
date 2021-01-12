import string
from typing import Sequence

from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.genes import CharGene
from evolutionary_algorithm.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)
from evolutionary_algorithm.selectors.tournament import Tournament

to_find = "welcome to yaga"


def evaluate(ind: Sequence[str]):
    joined_ind = "".join(ind)
    return sum((a == b) for a, b in zip(joined_ind, to_find))


def find_the_string():
    eva = (
        EvolutionaryAlgorithmBuilder(
            population_size=100,
            generations=600,
            individual_structure=UniformIndividualStructure(
                tuple(
                    CharGene(allowed_characters=string.ascii_lowercase + " ")
                    for _ in range(len(to_find))
                )
            ),
        )
        .selector(Tournament(tournament_size=3, selection_size=10))
        .add_operator(OnePointCrossoverOperator, 0.8)
        .add_operator(MutationOperator, 0.1)
        .initialize(evaluate)
    )
    eva.run()


if __name__ == "__main__":
    find_the_string()
