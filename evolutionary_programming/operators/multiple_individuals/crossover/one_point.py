import itertools
import random
from typing import Iterable, Sequence

from evolutionary_programming.individuals import IndividualType
from evolutionary_programming.individuals.individual_structure import G
from evolutionary_programming.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)


class OnePointCrossoverOperator(MultipleIndividualOperator[G]):
    def __call__(self, _parents: Iterable[IndividualType[G]]) -> IndividualType:
        _parent1, _parent2 = self.peek(_parents)
        crossover_point = random.randint(0, len(self.individual_structure) - 1)
        serialised_individual = itertools.chain(
            itertools.islice(_parent1, crossover_point),
            itertools.islice(_parent2, crossover_point, None),
        )
        return self.individual_structure.build_individual_from_genes_values(
            serialised_individual
        )

    def peek(self, it: Iterable[IndividualType[G]]) -> Sequence[IndividualType[G]]:
        return list(itertools.islice(it, 2))
