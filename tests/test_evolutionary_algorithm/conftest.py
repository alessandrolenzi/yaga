import pytest

from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.genes import IntGene
from evolutionary_programming.individuals import UniformIndividualStructure
from evolutionary_programming.ranker import Ranker
from evolutionary_programming.selectors.tournament import Tournament


@pytest.fixture
def default_evolutionary_algorithm() -> EvolutionaryAlgorithm:
    return EvolutionaryAlgorithm(
        population_size=10,
        generations=10,
        selector=Tournament(selection_size=2, tournament_size=10),
        ranker=Ranker(lambda x: 0),
        individual_structure=UniformIndividualStructure(
            tuple(IntGene(lower_bound=0, upper_bound=10) for _ in range(10))
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
    )
