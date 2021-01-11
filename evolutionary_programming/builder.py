from concurrent.futures._base import Executor
from typing import (
    Final,
    Callable,
    Generic,
    Tuple,
    List,
    Optional,
)

from evolutionary_programming.evolutionary_algorithm import (
    GeneType,
    EvolutionaryAlgorithm,
)
from evolutionary_programming.individuals import IndividualStructure
from evolutionary_programming.operators.base import GeneticOperator
from evolutionary_programming.operators.multiple_individuals.base import (
    MultipleIndividualOperator,
)
from evolutionary_programming.operators.single_individual.base import (
    SingleIndividualOperator,
)
from evolutionary_programming.ranker import Ranker, Q, IndividualType
from evolutionary_programming.selectors.selector import Selector


class EvolutionaryAlgorithmBuilder(Generic[IndividualType, GeneType]):
    population_size: Final[int]
    generations: Final[Optional[int]]

    def __init__(
        self,
        population_size: int,
        generations: Optional[int],
        *,
        individual_structure: IndividualStructure[IndividualType, GeneType],
        elite_size: int = 0,
    ):
        self.population_size = population_size
        self.generations = generations
        self._operators: List[Tuple[GeneticOperator, float]] = []
        self._indstr: Final = individual_structure
        self.elite_size = elite_size

    def selector(self, s: Selector):
        self._selector = s
        return self

    def executor(self, e: Executor):
        self._executor = e
        return self

    def add_operator(
        self,
        operator_builder: GeneticOperator[IndividualStructure, GeneType],
        execution_probability: float,
    ):
        self._operators.append((operator_builder, execution_probability))
        return self

    def initialize(self, score_function: Callable[[IndividualType], Q]):
        (
            multiple_individual_operators,
            single_individual_operators,
        ) = self._prepare_operators()
        return EvolutionaryAlgorithm(
            population_size=self.population_size,
            generations=self.generations,
            individual_structure=self._indstr,
            ranker=Ranker(score_function),
            selector=self._selector,
            multiple_individual_operators=multiple_individual_operators,
            single_individual_operators=single_individual_operators,
            elite_size=self.elite_size,
        )

    def _prepare_operators(self):
        multiple_operators: List[Tuple[MultipleIndividualOperator, float]] = []
        single_operators: List[Tuple[SingleIndividualOperator, float]] = []
        for operator, prob in self._operators:
            concrete = operator(self._indstr)
            if isinstance(concrete, MultipleIndividualOperator):
                multiple_operators.append((concrete, prob))
            else:
                single_operators.append((concrete, prob))
        return multiple_operators, single_operators
