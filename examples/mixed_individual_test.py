from yaga_ga.evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from yaga_ga.evolutionary_algorithm.genes import IntGene, FloatGene, CharGene
from yaga_ga.evolutionary_algorithm.individuals import (
    MixedIndividualStructure,
)
from yaga_ga.evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from yaga_ga.evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)
from yaga_ga.evolutionary_algorithm.selectors.tournament import Tournament

target = (0.111, 0.34, 128, "c", "a")


def evaluation(individual):
    ind = tuple(individual)
    first = sum(abs(i - j) for i, j in zip(ind[:3], target[:3]))
    return 500 - (
        first + sum(abs(ord(i[0]) - ord(j[0])) for i, j in zip(ind[3:], target[3:]))
    )


def find_mixed_individual():
    individual_structure = (
        MixedIndividualStructure(FloatGene(lower_bound=0, upper_bound=1))
        .add_gene(FloatGene(lower_bound=0, upper_bound=1))
        .add_gene(IntGene(lower_bound=0, upper_bound=129))
        .add_gene(CharGene())
        .add_gene(CharGene())
    )
    eva = (
        EvolutionaryAlgorithmBuilder(
            population_size=200,
            generations=2000,
            elite_size=10,
            individual_structure=individual_structure,
        )
        .selector(Tournament(tournament_size=3, selection_size=50))
        .add_operator(MutationOperator, 0.01)
        .add_operator(OnePointCrossoverOperator, 0.8)
        .initialize(evaluation)
    ).add_callback(lambda e: print(e.fittest))
    eva.run()


if __name__ == "__main__":
    find_mixed_individual()
