import string
from typing import Sequence

from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.genes import CharGene
from evolutionary_programming.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_programming.selectors.tournament import Tournament

to_find = "welcome to yaga"


def evaluate(ind: Sequence[str]):
    joined_ind = "".join(ind)
    return sum((a == b) for a, b in zip(joined_ind, to_find))


def find_the_string():
    eva = (
        EvolutionaryAlgorithm(population_size=100, generations=600, elite_ratio=0.01)
        .define_individual_structure(
            UniformIndividualStructure(
                tuple(
                    CharGene(allowed_characters=string.ascii_lowercase + " ")
                    for _ in range(len(to_find))
                )
            )
        )
        .define_selector(Tournament(tournament_size=3, selection_size=10))
        .initialize()
    )
    eva.run(evaluate)


if __name__ == "__main__":
    find_the_string()
