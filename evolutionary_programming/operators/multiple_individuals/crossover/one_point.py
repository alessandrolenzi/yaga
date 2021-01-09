import itertools
import random
from typing import Iterable, Sequence
from evolutionary_programming.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_programming.operators.protocols import (
    IterableIndividualType,
    GeneType,
)


class OnePointCrossoverOperator(
    MultipleIndividualOperator[IterableIndividualType[GeneType], GeneType]
):
    def __call__(
        self,
        base_individual: IterableIndividualType[GeneType],
        _parents: Iterable[IterableIndividualType[GeneType]],
    ) -> IterableIndividualType[GeneType]:
        parent1, parent2 = self.pick(base_individual, _parents)
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
        return random.randint(0, len(individual) - 1)
