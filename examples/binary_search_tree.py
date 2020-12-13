from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Type, Iterable

from evolutionary_programming.evolutionary_algorithm import EvolutionaryAlgorithm
from evolutionary_programming.individuals.gene_factory import GeneDefinition, IntGene
from evolutionary_programming.individuals.individual_structure import (
    IndividualStructure,
)
from evolutionary_programming.selectors.tournament import Tournament

T = TypeVar("T")


@dataclass
class Tree(Generic[T]):
    value: "T"
    left: "Optional[Tree[T]]" = None
    right: "Optional[Tree[T]]" = None

    def __iter__(self) -> "Iterable[T]":
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


def evaluate_binary_search_tree(t: Tree[int]):
    def _evaluate_recursive(t: Optional[Tree[int]]):
        if not t:
            return 0, 0, 0
        score, count, value = 0, 0, t.value
        if t.left:
            s, c, v = _evaluate_recursive(t.left)
            score += s + (t.left.value <= t.value)
            count += 1 + c
            value += v
        if t.right:
            s, c, v = _evaluate_recursive(t.right)
            score += s + (t.right.value >= t.value)
            count += 1 + c
            value += v
        return score, count, value

    score, count, value = _evaluate_recursive(t)
    return (score * value) / count


class TreeIndividualStructure(IndividualStructure[Tree[int]]):
    def __init__(self):
        super().__init__()
        self.root: Optional[Tree[GeneDefinition[int]]] = None
        self.current_node = None
        self.node_count = 0

    def define_gene(
        self: Type[T], gene_definition: GeneDefinition
    ) -> "TreeIndividualStructure[Tree[int]]":
        self.node_count += 1
        if not self.root:
            self.root = Tree(value=gene_definition)
            self.current_node = self.root
            return self
        if not self.current_node.left:
            self.current_node.left = Tree(value=gene_definition)
            return self
        if not self.current_node.right:
            self.current_node.right = Tree(value=gene_definition)
            self.current_node = self._find_first_free_position()
        return self

    def _find_first_free_position(self):
        q = [self.root]
        while q:
            current = q.pop()
            if current.left is None or current.right is None:
                return current
            if current.left:
                q.append(current.left)
            if current.right:
                q.append(current.left)

    def __len__(self):
        return self.node_count

    def __getitem__(self, item: int):
        queue = list()

        def _walk(position, current_node) -> Tree[GeneDefinition[int]]:
            if position == 0:
                return current_node
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
            next_element = queue.pop()
            return _walk(position - 1, next_element)

        return _walk(item, self.root).value

    def _iter_genes(self):
        return iter(self.root)

    def build(self):
        return self.build_individual_from_genes_values(
            i.generate() for i in self._iter_genes()
        )

    def build_individual_from_genes_values(self, value_iterator: Iterable[int]):
        to_fill_queue = list()
        root = None
        for i in value_iterator:
            if root is None:
                root = Tree(value=i)
                to_fill_queue.append(root)
                continue
            parent = to_fill_queue[0]
            if not parent.left:
                parent.left = Tree(value=i)
                to_fill_queue.append(parent.left)
                continue
            if not parent.right:
                parent.right = Tree(value=i)
                to_fill_queue.append(parent.right)
                to_fill_queue.pop(0)
        return root

    def freeze(self):
        self.frozen = True


def tree_structure(nodes: int):
    ind = TreeIndividualStructure()
    for _ in range(nodes):
        ind = ind.define_gene(IntGene(lower_bound=0, upper_bound=50))
    return ind


def find_binary_tree():
    eva = (
        EvolutionaryAlgorithm(population_size=200, generations=2000, elite_ratio=0.05)
        .define_individual_structure(tree_structure(30))
        .define_selector(Tournament(tournament_size=3, selection_size=50))
        .initialize()
    )
    eva.run(evaluate_binary_search_tree)


if __name__ == "__main__":
    find_binary_tree()
