import random
from typing import Iterable, Iterator, TypeVar

from yaga_ga.evolutionary_algorithm.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from yaga_ga.evolutionary_algorithm.operators.protocols import (
    SequentialIndividualType,
    GeneType,
    MultipleIndividualOperatorProtocol,
)


IndividualType = TypeVar("IndividualType", bound=SequentialIndividualType)


class UniformCrossoverOperator(
    MultipleIndividualOperator[IndividualType, GeneType],
    MultipleIndividualOperatorProtocol[IndividualType],
):
    def __call__(
        self,
        base_individual: IndividualType,
        _parents: Iterable[IndividualType],
    ) -> IndividualType:
        parents = self._pick(base_individual, _parents)

        def gene_selector() -> Iterator[GeneType]:
            for gene_for_all_parents in zip(*parents):
                selected = random.randrange(0, len(gene_for_all_parents))
                yield gene_for_all_parents[selected]

        return self.individual_structure.build_individual_from_genes_values(
            gene_selector()
        )
