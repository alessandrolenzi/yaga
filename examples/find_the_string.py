import string
from functools import partial
from typing import Sequence

from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.evolution import Evolution
from evolutionary_algorithm.genes import CharGene
from evolutionary_algorithm.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.multiple_individuals.crossover.uniform import (
    UniformCrossoverOperator,
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
    def callback(e: Evolution):
        if "".join(e.fittest) == to_find:
            e.stop()

    eva = (
        EvolutionaryAlgorithmBuilder(
            population_size=100,
            generations=None,
            individual_structure=UniformIndividualStructure(
                tuple(
                    CharGene(allowed_characters=string.ascii_lowercase + " ")
                    for _ in range(len(to_find))
                )
            ),
            elite_size=2,
        )
        .selector(Tournament(tournament_size=5, selection_size=50))
        .add_operator(partial(UniformCrossoverOperator, arity=5), 0.8)
        .add_operator(MutationOperator, 0.4)
        .add_callback(callback)
        .initialize(evaluate)
    )
    result = eva.run()
    print(f"Result found after {result.current_iteration} generations")


if __name__ == "__main__":
    find_the_string()
