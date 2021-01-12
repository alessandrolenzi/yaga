import itertools
import random
from dataclasses import dataclass
import string
from typing import Sequence, Optional, Iterable, Any, Tuple, List

from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.genes import CharGene, GeneDefinition
from evolutionary_algorithm.individuals import (
    UniformIndividualStructure,
    IndividualType,
)
from evolutionary_algorithm.individuals.individual_structure import (
    IndividualStructure,
    GeneType,
)
from evolutionary_algorithm.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import (
    OnePointCrossoverOperator,
)
from evolutionary_algorithm.operators.single_individual.mutation import (
    MutationOperator,
)
from evolutionary_algorithm.selectors.tournament import Tournament

to_find = ["welcome", "to", "yaga"]


@dataclass
class ComparableScore:
    subscores: Sequence[float]
    fullMatch: float

    def __eq__(self: "ComparableScore", other: Any) -> bool:
        if not isinstance(other, ComparableScore):
            return NotImplemented

        return self.fullMatch == other.fullMatch and self.subscores == other.subscores

    def __lt__(self: "ComparableScore", other: "ComparableScore") -> bool:
        return self.total < other.total

    def _subscores_lt(self, other):
        count_ours = 0
        count_theirs = 0
        for ours, theirs in zip(self.subscores, other.subscores):
            count_ours += int(ours <= theirs)
            count_theirs += int(ours > theirs)
        return count_ours <= count_theirs

    @property
    def total(self):
        return 0.5 * self.fullMatch + 0.5 * sum(self.subscores)


def evaluate(solution: Sequence[str]) -> ComparableScore:
    total = 0
    subscores = []
    for pos, word in enumerate(solution):
        joined_ind = "".join(word)
        subscores.append(sum((a == b) for a, b in zip(joined_ind, to_find[pos])))
        total += int(joined_ind == to_find[pos])
    fullMatch = float(total) / len(to_find)
    return ComparableScore(fullMatch=fullMatch, subscores=subscores)


class RandomStringGene(GeneDefinition[str]):
    def __init__(self, length: int, allowed_characters: Optional[str] = None):
        self.genes = [
            CharGene(allowed_characters=allowed_characters) for _ in range(length)
        ]
        self.length = length

    def generate(self) -> str:
        return "".join([gene.generate() for gene in self.genes])


class OneCharMutationOperator(MutationOperator[str]):
    def make_mutation(self, gene: GeneDefinition[str], gene_value: str) -> str:
        if isinstance(gene, RandomStringGene):
            mutated_char = random.randint(0, gene.length - 1)
            return (
                gene_value[:mutated_char]
                + gene.genes[mutated_char].generate()
                + gene_value[mutated_char + 1 :]
            )
        return super().make_mutation(gene, gene_value)


class PickBest(MultipleIndividualOperator[Tuple[str, ...], str]):
    def __init__(self, individual_structure: IndividualStructure[Tuple[str, ...], str]):

        super().__init__(individual_structure, arity=10)

    def __call__(
        self, first: Tuple[str, ...], it: Iterable[Tuple[str, ...]]
    ) -> Tuple[str, ...]:
        l = self._pick(first, it)
        scored_l = list(map(evaluate, l))
        accumulated = list(l.pop(0))
        first_score = scored_l.pop(0)
        for ind, score in zip(l, scored_l):
            for index, comp in enumerate(ind):
                if first_score.subscores[index] < score.subscores[index]:
                    accumulated[index] = comp
                    prev_scores = list(first_score.subscores)
                    prev_scores[index] = score.subscores[index]
                    first_score.subscores = prev_scores
        return tuple(first)


def find_multiple_strings():
    eva = (
        EvolutionaryAlgorithmBuilder(
            population_size=100,
            generations=1000,
            individual_structure=UniformIndividualStructure(
                tuple(
                    RandomStringGene(
                        allowed_characters=string.ascii_lowercase + " ", length=len(sub)
                    )
                    for sub in to_find
                )
            ),
        )
        .selector(Tournament(tournament_size=3, selection_size=40))
        .add_operator(OnePointCrossoverOperator, 0.8)
        .add_operator(OneCharMutationOperator, 0.1)
        .add_operator(PickBest, 0.1)
        .initialize(evaluate)
    )
    eva.run()


if __name__ == "__main__":
    find_multiple_strings()
