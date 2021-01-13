from inspect import signature
from typing import Iterable

import pytest
from doubles import expect

from evolutionary_algorithm.genes import IntGene
from evolutionary_algorithm.individuals import UniformIndividualStructure
from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.protocols import (
    MultipleIndividualOperatorProtocol,
    SingleIndividualOperatorProtocol,
)


@pytest.mark.parametrize("crossover_point", [0, 2, 5, 9, 50])
def test_one_point_crossover(crossover_point):
    individual_structure = UniformIndividualStructure(
        tuple(IntGene(lower_bound=0, upper_bound=10) for _ in range(10))
    )
    ind1 = individual_structure.build()
    ind2 = individual_structure.build()
    operator = OnePointCrossoverOperator(individual_structure)
    expect(operator).crossover_point.once().and_return(crossover_point)
    child = operator(ind1, [ind2])
    assert child[0:crossover_point] == ind1[0:crossover_point]
    assert child[crossover_point:] == ind2[crossover_point:]


# def test_isinstance():
#     individual_structure = UniformIndividualStructure(
#         tuple(IntGene(lower_bound=0, upper_bound=10) for _ in range(10))
#     )
#     operator = OnePointCrossoverOperator(individual_structure)
#     sig = signature(operator)
#     import pdb; pdb.set_trace()
#     assert isinstance(operator, MultipleIndividualOperatorProtocol)
#     assert not isinstance(operator, SingleIndividualOperatorProtocol)
#
# def test_isinstance_2():
#     individual_structure = UniformIndividualStructure(
#         tuple(IntGene(lower_bound=0, upper_bound=10) for _ in range(10))
#     )
#     def fakeop(i: UniformIndividualStructure[int], it: Iterable[UniformIndividualStructure[int]]) -> UniformIndividualStructure[int]:
#         return i
#
#     sig = signature(fakeop)
#     import pdb; pdb.set_trace()
#     assert isinstance(fakeop, MultipleIndividualOperatorProtocol)
#     assert not isinstance(fakeop, SingleIndividualOperatorProtocol)
