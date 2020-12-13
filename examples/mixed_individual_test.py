from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.individuals.gene_definition import (
    FloatGene,
    IntGene,
    CharGene,
)
from evolutionary_programming.individuals.mixed_individual import (
    MixedIndividualStructure,
)
from evolutionary_programming.selectors.tournament import Tournament

target = (0.111, 0.34, 128, "c", "a")


def evaluation(individual):
    ind = tuple(individual)
    first = sum(abs(i - j) for i, j in zip(ind[:3], target[:3]))
    return 500 - (
        first + sum(abs(ord(i[0]) - ord(j[0])) for i, j in zip(ind[3:], target[3:]))
    )


def test_mixed_individual():
    eva = (
        EvolutionaryAlgorithm(population_size=200, generations=2000, elite_ratio=0.05)
        .define_individual_structure(
            MixedIndividualStructure(FloatGene(lower_bound=0, upper_bound=1))
            .define_gene(FloatGene(lower_bound=0, upper_bound=1))
            .define_gene(IntGene(lower_bound=0, upper_bound=129))
            .define_gene(CharGene())
            .define_gene(CharGene())
        )
        .define_selector(Tournament(tournament_size=3, selection_size=50))
        .initialize()
    )
    eva.run(evaluation)


if __name__ == "__main__":
    test_mixed_individual()
