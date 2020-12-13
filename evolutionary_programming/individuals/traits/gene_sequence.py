from collections import abc
from typing import Union, Tuple, TypeVar, Sequence, Generic
from typing_extensions import Final

T = TypeVar('T')

class GeneSequenceTrait(Generic[T]):
    def __init__(self, genes: Union[Sequence[T], T]):
        self.genes: Final[Tuple[T, ...]] = self._to_tuple(genes)

    def _update_genes(self, gene: T) -> Tuple[T, ...]:
        return self.genes + (gene, )

    def __getitem__(self, item: int) -> T:
        if 0 <= item < len(self.genes):
            return self.genes[item]
        raise IndexError(f"No gene with id {item}")

    def __len__(self):
        return len(self.genes)

    @classmethod
    def _to_tuple(cls, genes: Union[Sequence[T], T]) -> Tuple[T, ...]:
        if isinstance(genes, tuple):
            return genes
        if isinstance(genes, abc.Sequence):
            return tuple(gene for gene in genes)
        return (genes, )

