import itertools
import random
from typing import Tuple, Iterable, TypeVar

from yaga_ga.evolutionary_algorithm.individuals import IndividualStructure
from yaga_ga.evolutionary_algorithm.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)

from yaga_ga.evolutionary_algorithm.operators.protocols import (
    SequentialIndividualType,
    GeneType,
    MultipleIndividualOperatorProtocol,
)

IndividualType = TypeVar("IndividualType", bound=SequentialIndividualType)


class TwoPointsCrossoverOperator(
    MultipleIndividualOperator[IndividualType, GeneType],
    MultipleIndividualOperatorProtocol[IndividualType],
):
    def __init__(
        self,
        individual_structure: IndividualStructure[IndividualType, GeneType],
        arity: int = 2,
    ):
        assert (
            arity > 1 and arity <= 3
        ), f"TwoPointsCrossoverOperator cannot have arity {arity} > 3: at most 3 parents can be used in this operation."
        super().__init__(individual_structure, arity=arity)

    def __call__(
        self,
        base_individual: IndividualType,
        _parents: Iterable[IndividualType],
    ) -> IndividualType:
        parents = self._pick(base_individual, _parents)
        first_crossover_point, second_crossover_point = self.crossover_points(
            parents[0]
        )
        return self.individual_structure.build_individual_from_genes_values(
            itertools.chain(
                itertools.islice(parents[0], 0, first_crossover_point),
                itertools.islice(
                    parents[1], first_crossover_point, second_crossover_point
                ),
                itertools.islice(
                    parents[2 % len(parents)], second_crossover_point, None
                ),
            )
        )

    def crossover_points(
        self, individual: SequentialIndividualType[GeneType]
    ) -> Tuple[int, int]:
        first_crossover_point = random.randrange(0, len(individual))
        second_crossover_point = random.randrange(
            first_crossover_point, len(individual)
        )
        return first_crossover_point, second_crossover_point
