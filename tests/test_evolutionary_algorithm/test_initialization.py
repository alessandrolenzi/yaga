from doubles import expect

from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm


def test_can_set_initial_population(
    default_evolutionary_algorithm: EvolutionaryAlgorithm,
):
    ind1 = default_evolutionary_algorithm.individual_structures.build()
    ind2 = default_evolutionary_algorithm.individual_structures.build()
    default_evolutionary_algorithm.set_initial_population([ind1, ind2])
    assert ind1 in default_evolutionary_algorithm._population
    assert ind2 in default_evolutionary_algorithm._population


def test_ensure_initial_population_generates_right_number_of_individuals(
    default_evolutionary_algorithm: EvolutionaryAlgorithm,
):
    default_evolutionary_algorithm.ensure_population_initialized()
    assert (
        len(default_evolutionary_algorithm._population)
        == default_evolutionary_algorithm.population_size
    )


def test_ensure_run_initialises_population(
    default_evolutionary_algorithm: EvolutionaryAlgorithm,
):
    default_evolutionary_algorithm.run()
    assert (
        len(default_evolutionary_algorithm._population)
        == default_evolutionary_algorithm.population_size
    )


def test_initial_population_is_preserved(
    default_evolutionary_algorithm: EvolutionaryAlgorithm,
):
    ind1 = default_evolutionary_algorithm.individual_structures.build()
    ind2 = default_evolutionary_algorithm.individual_structures.build()
    default_evolutionary_algorithm.set_initial_population([ind1, ind2])
    assert ind1 in default_evolutionary_algorithm._population
    assert ind2 in default_evolutionary_algorithm._population
    default_evolutionary_algorithm.ensure_population_initialized()
    assert ind1 in default_evolutionary_algorithm._population
    assert ind2 in default_evolutionary_algorithm._population
    assert (
        len(default_evolutionary_algorithm._population)
        == default_evolutionary_algorithm.population_size
    )
