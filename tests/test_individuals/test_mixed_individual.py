from evolutionary_algorithm.genes import IntGene, CharGene
from evolutionary_algorithm.individuals.mixed_individual import (
    MixedIndividualStructure,
)


def test_initialization_with_tuple():
    gene_1 = CharGene()
    gene_2 = IntGene(lower_bound=1, upper_bound=1)
    individual = MixedIndividualStructure((gene_1, gene_2))
    assert len(individual) == 2
    built = individual.build()
    assert type(built[0]) == str
    assert type(built[1]) == int
    assert individual[0] == gene_1
    assert individual[1] == gene_2


def test_progressive_initialization():
    gene_1 = CharGene()
    gene_2 = IntGene(lower_bound=1, upper_bound=1)
    individual = MixedIndividualStructure(gene_1)
    assert len(individual) == 1
    built = individual.build()
    assert len(built) == 1
    assert type(built[0]) == str
    individual_2 = individual.add_gene(gene_2)
    assert len(individual_2) == 2
    assert individual_2[0] == gene_1
    assert individual_2[1] == gene_2
    built2 = individual_2.build()
    assert len(built2) == 2
    assert type(built2[0]) == str
    assert type(built2[1]) == int
