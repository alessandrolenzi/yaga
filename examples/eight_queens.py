import itertools
from typing import Tuple, Iterable, Mapping, Sequence

from evolutionary_algorithm.builder import EvolutionaryAlgorithmBuilder
from evolutionary_algorithm.evolution import Evolution
from evolutionary_algorithm.genes import GeneDefinition, random
from evolutionary_algorithm.individuals import IndividualStructure
from evolutionary_algorithm.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_algorithm.operators.single_individual.base import (
    SingleIndividualOperator,
)
from evolutionary_algorithm.selectors.tournament import Tournament


QueenPositions = Mapping[int, int]
Position = Tuple[int, int]


class UniqueRowColPermutation(GeneDefinition[Sequence[Position]]):
    def __init__(self, board_size: int):
        self.board_size = board_size

    def generate(self) -> Sequence[Position]:
        rows_indexes = [i for i in range(self.board_size)]
        cols_indexes = [i for i in range(self.board_size)]
        random.shuffle(rows_indexes)
        random.shuffle(cols_indexes)
        return list(p for p in zip(rows_indexes, cols_indexes))


class BoardConfiguration(IndividualStructure[QueenPositions, Position]):
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.gene = UniqueRowColPermutation(board_size=board_size)

    def build(self) -> QueenPositions:
        return {k: v for k, v in self.gene.generate()}

    def build_individual_from_genes_values(
        self, it: Iterable[Position]
    ) -> QueenPositions:
        return {k: v for k, v in it}


class RandomBoard(SingleIndividualOperator):
    def __init__(self, individual_structure: BoardConfiguration):
        super().__init__(individual_structure)

    def __call__(self, _parent1: QueenPositions) -> QueenPositions:
        return self.individual_structure.build()


class SwapColumnsOperator(SingleIndividualOperator):
    def __init__(self, individual_structure: BoardConfiguration):
        super().__init__(individual_structure)

    def __call__(self, selected: QueenPositions) -> QueenPositions:
        start_pos = random.randrange(0, len(selected))
        end_pos = random.randrange(0, len(selected))
        final = {k: v for k, v in selected.items()}
        final[start_pos], final[end_pos] = final[end_pos], final[start_pos]
        return self.individual_structure.build_individual_from_genes_values(
            final.items()
        )


class MixBoardsOperator(MultipleIndividualOperator[QueenPositions, Tuple[int, int]]):
    def __call__(
        self, selected: QueenPositions, others: Iterable[QueenPositions]
    ) -> QueenPositions:
        parent_1, parent_2 = self._pick(selected, others)
        start_point = random.randrange(0, len(parent_1))
        end_point = random.randrange(start_point, len(parent_1))
        parent_1_selected_genome = {
            k: v for k, v in parent_1.items() if k >= start_point and k <= end_point
        }
        selected_cols = set(parent_1_selected_genome.values())
        child = {
            **{k: v for k, v in parent_2.items() if v not in selected_cols},
            **parent_1_selected_genome,
        }
        missing_rows = set(parent_1.keys()) - set(child.keys())
        missing_cols = set(parent_1.values()) - set(child.values())
        assert len(missing_cols) == len(missing_cols)
        child.update({row: col for row, col in zip(missing_rows, missing_cols)})
        return self.individual_structure.build_individual_from_genes_values(
            (k, v) for k, v in child.items()
        )


def conflicts(board_size, q) -> int:
    col_conflicts = board_size - len(set(v for v in q.values()))
    return col_conflicts + int(
        sum(_diagonal_conflicts(board_size, q, pos) for pos in q.items()) / 2
    )


def _diagonal_conflicts(board_size, q, position: Position) -> int:
    total_conflicts = 0
    y_pos, x_pos = position
    for y_incr, x_incr in itertools.product((-1, -1), (1, -1)):
        limit_y = board_size if y_incr > 0 else -1
        limit_x = board_size if x_incr > 0 else -1
        for i, j in zip(
            range(y_pos + y_incr, limit_y, y_incr),
            range(x_pos + x_incr, limit_x, x_incr),
        ):
            if q[i] == j:
                total_conflicts += 1
    return total_conflicts


def evaluation_function(q: QueenPositions) -> int:
    return -conflicts(8, q)


def solve_eight_queens():
    eva = (
        EvolutionaryAlgorithmBuilder(
            population_size=50,
            generations=None,
            individual_structure=BoardConfiguration(board_size=8),
            elite_size=10,
        )
        .selector(Tournament(selection_size=30, tournament_size=5))
        .add_operator(RandomBoard, 0.02)
        .add_operator(SwapColumnsOperator, 0.4)
        .add_operator(MixBoardsOperator, 0.5)
        .initialize(evaluation_function)
    )
    found_it = 0

    def callback(e: Evolution):
        nonlocal found_it
        if e.fittest_score == 0:
            e.stop()
            print(f"Solution found at iteration {e.current_iteration}!")
            print(e.fittest)
            found_it = e.current_iteration

    eva._iterations_callback.append(callback)
    eva.run()
    return found_it


if __name__ == "__main__":
    solve_eight_queens()
