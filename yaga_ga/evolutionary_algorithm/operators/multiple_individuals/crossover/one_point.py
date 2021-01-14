import itertools
import random
from typing import Iterable, Sequence, TypeVar

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


class OnePointCrossoverOperator(
    MultipleIndividualOperator[IndividualType, GeneType],
    MultipleIndividualOperatorProtocol[IndividualType],
):
    def __init__(
        self, individual_structure: IndividualStructure[IndividualType, GeneType]
    ):
        super().__init__(individual_structure, arity=2)

    def __call__(
        self,
        base_individual: IndividualType,
        _parents: Iterable[IndividualType],
    ) -> IndividualType:
        parent1, parent2 = self._pick(base_individual, _parents)
        _parent1_sequence = [i for i in parent1]
        crossover_point = self.crossover_point(_parent1_sequence)
        serialised_individual = itertools.chain(
            itertools.islice(_parent1_sequence, crossover_point),
            itertools.islice(parent2, crossover_point, None),
        )
        return self.individual_structure.build_individual_from_genes_values(
            serialised_individual
        )

    def crossover_point(self, individual: Sequence[GeneType]) -> int:
        return random.randrange(0, len(individual))
