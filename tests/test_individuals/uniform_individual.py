from evolutionary_programming.individuals.gene_definition import CharGene
from evolutionary_programming.individuals.uniform_individual import \
    UniformIndividualStructure


def test_initialisation_with_tuple():
    gene_1 = CharGene()
    gene_2 = CharGene()
    individual = UniformIndividualStructure(
        (gene_1, gene_2)
    )
    assert len(individual) == 2
    assert len(individual.build()) == 2
    assert individual[0] == gene_1
    assert individual[1] == gene_2
