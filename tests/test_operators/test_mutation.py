import pytest
from doubles import allow

from evolutionary_algorithm.genes import IntGene
from evolutionary_algorithm.individuals import UniformIndividualStructure
from evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)


@pytest.mark.parametrize("genes_to_mutate", [1, 2, 3, 4, 5, 6])
def test_mutation_generates_right_number_of_mutations(genes_to_mutate):
    individual_structure = UniformIndividualStructure(
        tuple(IntGene(lower_bound=0, upper_bound=5) for _ in range(5))
    )
    ind = individual_structure.build()
    for gene_definition in individual_structure:
        allow(gene_definition).generate.once().and_return(6)
    mutation_operator = MutationOperator(
        individual_structure, genes_to_mutate=genes_to_mutate
    )
    mutated = mutation_operator(ind)
    assert ind != mutated
    assert sum(int(i == 6) for i in mutated) == min(genes_to_mutate, 5)
    assert sum(int(i == j) for i, j in zip(ind, mutated)) == 5 - min(genes_to_mutate, 5)
