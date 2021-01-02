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
        self, _parents: Iterable[IterableIndividualType[GeneType]]
    ) -> IterableIndividualType[GeneType]:
        _parent1, _parent2 = self.peek(_parents)
        _parent_1_fenotype = [i for i in _parent1]
        crossover_point = random.randint(0, len(_parent_1_fenotype) - 1)
        serialised_individual = itertools.chain(
            itertools.islice(_parent_1_fenotype, crossover_point),
            itertools.islice(_parent2, crossover_point, None),
        )
        return self.individual_structure.build_individual_from_genes_values(
            serialised_individual
        )

    def peek(
        self, it: Iterable[IterableIndividualType[GeneType]]
    ) -> Sequence[IterableIndividualType[GeneType]]:
        return list(itertools.islice(it, 2))
