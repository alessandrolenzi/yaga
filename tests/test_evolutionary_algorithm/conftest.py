from typing import Tuple, Callable

import pytest

from yaga_ga.evolutionary_algorithm.evolutionary_algorithm import EvolutionaryAlgorithm
from yaga_ga.evolutionary_algorithm.genes import IntGene
from yaga_ga.evolutionary_algorithm.individuals import UniformIndividualStructure
from yaga_ga.evolutionary_algorithm.ranker import Ranker
from yaga_ga.evolutionary_algorithm.selectors.tournament import Tournament


@pytest.fixture
def default_score_function() -> Callable[[Tuple[int, ...]], float]:
    def _inner(individual: Tuple[int, ...]) -> float:
        return float(sum(individual)) / len(individual)

    return _inner


@pytest.fixture
def default_evolutionary_algorithm(default_score_function) -> EvolutionaryAlgorithm:
    return EvolutionaryAlgorithm(
        population_size=10,
        generations=10,
        selector=Tournament(selection_size=2, tournament_size=10),
        ranker=Ranker(default_score_function),
        individual_structure=UniformIndividualStructure(
            tuple(IntGene(lower_bound=0, upper_bound=10) for _ in range(10))
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
    )
