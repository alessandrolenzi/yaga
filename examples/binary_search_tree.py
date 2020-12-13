from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Type, Iterable, Union, Tuple, Iterator

from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.individuals.gene_definition import IntGene, GeneDefinition
from evolutionary_programming.individuals.uniform_individual import (
    UniformIndividualStructure,
    GenesType,
    IndividualStructure,
)
from evolutionary_programming.individuals.uniform_individual import (
    UniformIndividualStructure,
)
from evolutionary_programming.selectors.tournament import Tournament

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
        (t.left is None or t.left.value <= value) and
        (t.right is None or t.right.value >= value) and
        _is_bst(t.left) and
        _is_bst(t.right)
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
    return (_evaluate_recursive(t) / 30) * _tot_values_held


class TreeIndividualStructure(UniformIndividualStructure[GenesType]):
    def __init__(
        self,
        genes: Union[Tuple[GeneDefinition[GenesType], ...], GeneDefinition[GenesType]],
    ):
        super().__init__(genes, individual_class=Tree.from_values)


def tree_structure(nodes: int):
    return TreeIndividualStructure(
        tuple(IntGene(lower_bound=0, upper_bound=50) for _ in range(nodes))
    )


def find_binary_tree():
    eva = (
        EvolutionaryAlgorithm(population_size=200, generations=2000, elite_ratio=0.05)
        .define_individual_structure(tree_structure(30))
        .define_selector(Tournament(tournament_size=3, selection_size=50))
        .initialize()
    )
    result, score = eva.run(evaluate_binary_search_tree)
    print(f"result is binary search tree? {_is_bst(result)}, {score}")
    all_values = tuple(i for i in result)
    print(f"average value is {sum(all_values)/len(all_values)}")


if __name__ == "__main__":
    find_binary_tree()
