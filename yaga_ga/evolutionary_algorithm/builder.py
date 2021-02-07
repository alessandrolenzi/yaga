from concurrent.futures._base import Executor
from typing import (
    Callable,
    Generic,
    Tuple,
    List,
    Optional,
    Union,
    cast,
)

from mypy_extensions import DefaultNamedArg
from typing_extensions import Final
from inspect import signature

from yaga_ga.evolutionary_algorithm.evolution import Evolution
from yaga_ga.evolutionary_algorithm.evolutionary_algorithm import (
    GeneType,
    EvolutionaryAlgorithm,
)
from yaga_ga.evolutionary_algorithm.individuals import IndividualStructure
from yaga_ga.evolutionary_algorithm.operators.protocols import (
    MultipleIndividualOperatorProtocol,
    SingleIndividualOperatorProtocol,
)
from yaga_ga.evolutionary_algorithm.ranker import Ranker, Q, IndividualType
from yaga_ga.evolutionary_algorithm.selectors.selector import Selector


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
        self._multiple_individual_operators: List[
            Tuple[MultipleIndividualOperatorProtocol[IndividualType], float]
        ] = []
        self._single_individual_operators: List[
            Tuple[SingleIndividualOperatorProtocol[IndividualType], float]
        ] = []
        self._individual_structure: Final = individual_structure
        self.elite_size = elite_size
        self._callbacks: List[Callable[[Evolution], None]] = []
        self._executor: Optional[Executor] = None
        self._selector: Optional[Selector] = None
        self._ranker: Callable[
            [
                Callable[[IndividualType], Q],
                DefaultNamedArg(Optional[Executor], "executor"),
            ],
            Ranker,
        ] = Ranker

    def selector(self, s: Selector):
        self._selector = s
        return self

    def ranker_type(
        self,
        r: Callable[
            [
                Callable[[IndividualType], Q],
                DefaultNamedArg(Optional[Executor], "executor"),
            ],
            Ranker,
        ],
    ):
        self._ranker = r
        return self

    def executor(self, e: Executor):
        self._executor = e
        return self

    def add_operator(
        self,
        operator_builder: Callable[
            [IndividualStructure],
            Union[
                MultipleIndividualOperatorProtocol[IndividualType],
                SingleIndividualOperatorProtocol[IndividualType],
            ],
        ],
        execution_probability: float,
    ):
        self.add_operator_instance(
            operator_builder(self._individual_structure), execution_probability
        )
        return self

    def add_operator_instance(
        self,
        operator: Union[
            MultipleIndividualOperatorProtocol[IndividualType],
            SingleIndividualOperatorProtocol[IndividualType],
        ],
        execution_probability: float,
    ):
        if self._is_multiple_individual_op(operator):
            self._multiple_individual_operators.append(
                (
                    cast(MultipleIndividualOperatorProtocol[IndividualType], operator),
                    execution_probability,
                )
            )
        elif self._is_single_individual_op(operator):
            self._single_individual_operators.append(
                (
                    cast(SingleIndividualOperatorProtocol[IndividualType], operator),
                    execution_probability,
                )
            )
        else:
            raise TypeError(
                "The specified operator is not supported; you must respect MultipleIndividualOperatorProtocol or SingleIndividualOperator protocol."
            )
        return self

    def initialize(self, score_function: Callable[[IndividualType], Q]):
        if self._selector:
            return EvolutionaryAlgorithm(
                population_size=self.population_size,
                generations=self.generations,
                individual_structure=self._individual_structure,
                ranker=self._ranker(score_function, executor=self._executor),
                selector=self._selector,
                multiple_individual_operators=self._multiple_individual_operators,
                single_individual_operators=self._single_individual_operators,
                elite_size=self.elite_size,
                iteration_callbacks=self._callbacks,
            )
        assert False, "Must specify selector!"

    def add_callback(self, callback: Callable[[Evolution], None]):
        self._callbacks.append(callback)
        return self

    @staticmethod
    def _is_single_individual_op(
        operator: Union[
            MultipleIndividualOperatorProtocol[IndividualType],
            SingleIndividualOperatorProtocol[IndividualType],
        ]
    ):
        return (
            isinstance(operator, SingleIndividualOperatorProtocol)
            and len(signature(operator).parameters) == 1
        )

    @staticmethod
    def _is_multiple_individual_op(
        operator: Union[
            MultipleIndividualOperatorProtocol[IndividualType],
            SingleIndividualOperatorProtocol[IndividualType],
        ]
    ):
        return (
            isinstance(operator, MultipleIndividualOperatorProtocol)
            and len(signature(operator).parameters) == 2
        )
