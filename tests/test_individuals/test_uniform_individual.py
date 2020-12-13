import pytest

from evolutionary_programming.individuals.gene_definition import CharGene
from evolutionary_programming.individuals.individual_structure import \
    InvalidIndividual
from evolutionary_programming.individuals.uniform_individual import \
    UniformIndividualStructure


def test_initialization_with_tuple():
    gene_1 = CharGene()
    gene_2 = CharGene()
    individual = UniformIndividualStructure(
        (gene_1, gene_2)
    )
    assert len(individual) == 2
    assert len(individual.build()) == 2
    assert individual[0] == gene_1
    assert individual[1] == gene_2

def test_progressive_initialization():
    gene_1 = CharGene()
    gene_2 = CharGene()
    individual = UniformIndividualStructure(gene_1)
    assert len(individual) == 1
    assert len(individual.build()) == 1
    individual_2 = individual.define_gene(gene_2)
    assert len(individual_2) == 2
    assert len(individual_2.build()) == 2
    assert individual_2[0] == gene_1
    assert individual_2[1] == gene_2


def test_build_individual_from_gene_values_raises_with_wrong_number_of_values():
        UniformIndividualStructure(
            (CharGene(), CharGene())
        ).build_individual_from_genes_values([1, 2, 3])

