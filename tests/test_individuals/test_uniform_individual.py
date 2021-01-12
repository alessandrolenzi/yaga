import pytest

from evolutionary_algorithm.genes import CharGene
from evolutionary_algorithm.individuals.uniform_individual import (
    UniformIndividualStructure,
)


def test_initialization_with_tuple():
    gene_1 = CharGene()
    gene_2 = CharGene()
    individual = UniformIndividualStructure((gene_1, gene_2))
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
    individual_2 = individual.add_gene(gene_2)
    assert len(individual_2) == 2
    assert len(individual_2.build()) == 2
    assert individual_2[0] == gene_1
    assert individual_2[1] == gene_2


def test_getitem_is_correct():
    individual = UniformIndividualStructure(CharGene())
    assert individual[0]
    with pytest.raises(IndexError):
        _ = individual[1]
