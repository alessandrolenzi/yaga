import itertools
import random
from collections import Iterable
from typing import Tuple

from evolutionary_algorithm.individuals import IndividualStructure
from evolutionary_algorithm.operators.multiple_individuals.base import \
    MultipleIndividualOperator
from evolutionary_algorithm.operators.protocols import \
    SequentialIndividualType, GeneType


class TwoPointsCrossoverOperator(
    MultipleIndividualOperator[SequentialIndividualType[GeneType], GeneType]
):
    def __init__(self, individual_structure: IndividualStructure[SequentialIndividualType[GeneType], GeneType], arity: int = 2):
        assert arity >1 and arity <= 3, f"TwoPointsCrossoverOperator cannot have arity {arity} > 3: at most 3 parents can be used in this operation."
        super().__init__(individual_structure, arity=arity)

    def __call__(
            self,
            base_individual: SequentialIndividualType[GeneType],
            _parents: Iterable[SequentialIndividualType[GeneType]],
    ) -> SequentialIndividualType[GeneType]:
        parents = self._pick(base_individual, _parents)
        first_crossover_point, second_crossover_point = self.crossover_points(parents[0])
        return self.individual_structure.build_individual_from_genes_values(
            itertools.chain(
                itertools.islice(parents[0], 0, first_crossover_point),
                itertools.islice(parents[1], first_crossover_point, second_crossover_point),
                itertools.islice(parents[2 % len(parents)], second_crossover_point, None),
            )
        )

    def crossover_points(self, individual: SequentialIndividualType[GeneType]) -> Tuple[int, int]:
        first_crossover_point = random.randrange(0, len(individual))
        second_crossover_point = random.randrange(first_crossover_point,
                                                  len(individual))
        return first_crossover_point, second_crossover_point




