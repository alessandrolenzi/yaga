import random
from typing import Iterable, Iterator

from evolutionary_algorithm.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_algorithm.operators.protocols import (
    SequentialIndividualType,
    GeneType,
)


class UniformCrossoverOperator(
    MultipleIndividualOperator[SequentialIndividualType[GeneType], GeneType]
):
    def __call__(
        self,
        base_individual: SequentialIndividualType[GeneType],
        _parents: Iterable[SequentialIndividualType[GeneType]],
    ) -> SequentialIndividualType[GeneType]:
        parents = self._pick(base_individual, _parents)

        def gene_selector() -> Iterator[GeneType]:
            for gene_for_all_parents in zip(*parents):
                selected = random.randrange(0, len(gene_for_all_parents))
                yield gene_for_all_parents[selected]

        return self.individual_structure.build_individual_from_genes_values(
            gene_selector()
        )
