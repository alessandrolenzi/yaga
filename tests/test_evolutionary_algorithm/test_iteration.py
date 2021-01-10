from copy import copy

from doubles import expect

from evolutionary_programming.evolution import Evolution
from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.genes import IntGene
from evolutionary_programming.individuals import UniformIndividualStructure
from evolutionary_programming.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_programming.operators.single_individual.mutation import (
    MutationOperator,
)
from evolutionary_programming.ranker import Ranker
from evolutionary_programming.selectors.random import Random


def test_iteration_calls_ranker():
    ranker = Ranker(lambda x: 1.0)
    assert not ranker.ranked_population
    eva = EvolutionaryAlgorithm(
        ranker=ranker,
        selector=Random(selection_size=1),
        population_size=1,
        generations=1,
        individual_structure=UniformIndividualStructure(
            IntGene(lower_bound=0, upper_bound=1)
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
    )
    eva.run()
    assert len(eva._population) == len(ranker.ranked_population)
    assert set(eva._population) == set(r[0] for r in ranker.ranked_population)


def test_iteration_calls_selector():
    selector = Random(selection_size=1)
    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=selector,
        population_size=1,
        generations=1,
        individual_structure=UniformIndividualStructure(
            IntGene(lower_bound=0, upper_bound=1)
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
    )
    expect(selector).__call__.once().and_return([(1,)])
    eva.run()
    assert eva._population[0] == (1,)


def test_iteration_calls_single_individual_operators():
    individual_structure = UniformIndividualStructure(
        IntGene(lower_bound=0, upper_bound=1)
    )
    mutation_operator = MutationOperator(individual_structure)
    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=Random(selection_size=1),
        population_size=1,
        generations=1,
        individual_structure=individual_structure,
        multiple_individual_operators=[],
        single_individual_operators=[(mutation_operator, 1)],
    )
    expect(mutation_operator).__call__.once().and_return((1,))
    eva.run()
    assert eva._population[0] == (1,)


def test_iteration_regenerates_right_sized_population():
    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=Random(selection_size=1),
        population_size=5,
        generations=1,
        individual_structure=UniformIndividualStructure(
            IntGene(lower_bound=0, upper_bound=1)
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
    )
    eva.run()
    assert len(eva._population) == 5


def test_iteration_preserves_elites():
    ranker = Ranker(lambda x: 1.0)
    expect(ranker).rank.once()
    ranker.ranked_population = [((0,), 3)] + [((1,), 0)] * 4
    selector = Random(selection_size=1)
    expect(selector).__call__.once().and_return([(1,)])
    eva = EvolutionaryAlgorithm(
        ranker=ranker,
        selector=selector,
        population_size=5,
        generations=1,
        individual_structure=UniformIndividualStructure(
            IntGene(lower_bound=0, upper_bound=1)
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
        elite_size=1,
    )
    # invert order, to make sure that we're indeed selecting the elites.
    eva.set_initial_population(ranker.ranked_population[-1:])
    eva.run()
    assert eva._population[0] == (0,)
    assert len(eva._population) == 5


def test_iteration_calls_multiple_instances_of_single_individual_operator():
    individual_structure = UniformIndividualStructure(
        IntGene(lower_bound=0, upper_bound=1)
    )
    mutation_operator = MutationOperator(individual_structure)
    mutation_operator_2 = MutationOperator(individual_structure)
    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=Random(selection_size=1),
        population_size=1,
        generations=1,
        individual_structure=individual_structure,
        multiple_individual_operators=[],
        single_individual_operators=[(mutation_operator, 1), (mutation_operator_2, 1)],
    )
    expect(mutation_operator).__call__.once().and_return((1,))
    expect(mutation_operator_2).__call__.once().with_args((1,)).and_return((0,))
    eva.run()
    assert eva._population[0] == (0,)


def test_iteration_calls_multiple_individual_operator():
    individual_structure = UniformIndividualStructure(
        IntGene(lower_bound=0, upper_bound=1)
    )
    crossover_operator = OnePointCrossoverOperator(individual_structure)
    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=Random(selection_size=1),
        population_size=1,
        generations=1,
        individual_structure=individual_structure,
        multiple_individual_operators=[(crossover_operator, 1)],
        single_individual_operators=[],
    )
    expect(crossover_operator).__call__.once().and_return((1,))
    eva.run()
    assert eva._population[0] == (1,)


def test_iteration_calls_two_multiple_individual_operator():
    individual_structure = UniformIndividualStructure(
        IntGene(lower_bound=0, upper_bound=1)
    )
    crossover_operator = OnePointCrossoverOperator(individual_structure)
    crossover_operator_2 = OnePointCrossoverOperator(individual_structure)
    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=Random(selection_size=1),
        population_size=1,
        generations=1,
        individual_structure=individual_structure,
        multiple_individual_operators=[
            (crossover_operator, 1),
            (crossover_operator_2, 1),
        ],
        single_individual_operators=[],
    )
    eva.set_initial_population([(1,)])
    expect(crossover_operator).__call__.once().and_return((1,))
    expect(crossover_operator_2).__call__.once().with_args((1,), [(1,)]).and_return(
        (0,)
    )
    eva.run()
    assert eva._population[0] == (0,)


def test_iterations_calls_callback():
    counter = 0

    def callback(_: Evolution):
        nonlocal counter
        counter += 1

    eva = EvolutionaryAlgorithm(
        ranker=Ranker(lambda x: 1.0),
        selector=Random(selection_size=1),
        population_size=1,
        generations=1,
        individual_structure=UniformIndividualStructure(
            IntGene(lower_bound=0, upper_bound=1)
        ),
        multiple_individual_operators=[],
        single_individual_operators=[],
        iteration_callbacks=[callback],
    )
    eva.run()
    assert counter == 1
