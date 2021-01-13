from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
    Optional,
    Type,
    Iterable,
    Union,
    Iterator,
    Sequence,
)
from typing_extensions import Final

from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.genes.gene_definition import GeneDefinition
from evolutionary_algorithm.genes import IntGene
from evolutionary_algorithm.individuals import IndividualStructure
from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.multiple_individuals.crossover.uniform import (
    UniformCrossoverOperator,
)
from evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)
from evolutionary_algorithm.ranker import Ranker
from evolutionary_algorithm.selectors import Ranking
from evolutionary_algorithm.selectors.tournament import Tournament

T = TypeVar("T")
TreeType = TypeVar("TreeType", bound="Tree")


@dataclass
class Tree(Generic[T]):
    value: T
    left: "Optional[Tree[T]]" = None
    right: "Optional[Tree[T]]" = None

    def __iter__(self) -> Iterator[T]:
        q = [self]
        while q:
            current = q.pop(0)
            if current.left:
                q.append(current.left)
            if current.right:
                q.append(current.right)
            yield current.value

    @property
    def height(self):
        left_height = 0 if self.left is None else self.left.height
        right_height = 0 if self.right is None else self.right.height
        return 1 + max(left_height, right_height)

    @classmethod
    def from_values(cls: Type[TreeType], values: Iterable[T]) -> TreeType:
        to_fill_queue = list()
        root = None
        for value in values:
            if root is None:
                root = cls(value=value)
                to_fill_queue.append(root)
                continue
            parent = to_fill_queue[0]
            if not parent.left:
                parent.left = cls(value=value)
                to_fill_queue.append(parent.left)
                continue
            if not parent.right:
                parent.right = cls(value=value)
                to_fill_queue.append(parent.right)
                to_fill_queue.pop(0)
        if root is None:
            raise ValueError("Specify at least one value.")
        return root


def _is_bst(t: Optional[Tree[int]]):
    if t is None:
        return True
    value = t.value
    return (
        (t.left is None or t.left.value <= value)
        and (t.right is None or t.right.value >= value)
        and _is_bst(t.left)
        and _is_bst(t.right)
    )


def evaluate_binary_search_tree(t: Tree[int]):
    def _evaluate_recursive(t: Tree[int]):
        q = [t]
        binary_trees = 0
        while q:
            first = q.pop(0)
            if first.left:
                q.append(first.left)
            if first.right:
                q.append(first.right)
            binary_trees += int(_is_bst(first))

        return binary_trees

    _tot_values_held = sum(i for i in t)
    return ((_evaluate_recursive(t) - 15) / 30) * _tot_values_held


class TreeIndividualStructure(IndividualStructure[Tree[int], int]):

    genes: Final[Tree[GeneDefinition[int]]]

    def __init__(
        self, genes: Union[Sequence[GeneDefinition[int]], GeneDefinition[int]]
    ):
        _genes = [genes] if isinstance(genes, GeneDefinition) else genes
        self.genes = Tree.from_values(_genes)

    def build(self) -> Tree[int]:
        return Tree.from_values(i.generate() for i in self.genes)

    def build_individual_from_genes_values(self, it: Iterable[int]) -> Tree[int]:
        return Tree.from_values(i for i in it)

    def _update_genes(self, gene: GeneDefinition[int]) -> Tree[GeneDefinition[int]]:
        return Tree.from_values(tuple(iter(self.genes)) + (gene,))

    def __iter__(self):
        return iter(self.genes)


def tree_structure(nodes: int):
    return TreeIndividualStructure(
        tuple(IntGene(lower_bound=0, upper_bound=50) for _ in range(nodes))
    )


def find_binary_tree():
    eva = (
        EvolutionaryAlgorithmBuilder(
            population_size=200,
            generations=500,
            elite_size=20,
            individual_structure=tree_structure(30),
        )
        .selector(Ranking(selection_size=10))
        .add_operator(MutationOperator, 0.1)
        .add_operator(UniformCrossoverOperator, 0.9)
        .initialize(evaluate_binary_search_tree)
    )
    evolution = eva.run()
    print(
        f"result is binary search tree? {_is_bst(evolution.fittest)}, {evolution.fittest_score}"
    )
    all_values = tuple(i for i in evolution.fittest)
    print(f"average value is {sum(all_values)/len(all_values)}")


if __name__ == "__main__":
    find_binary_tree()
