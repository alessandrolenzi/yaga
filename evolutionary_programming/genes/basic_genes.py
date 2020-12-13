import random
import string
from typing import Optional, Sequence
from .gene_definition import GeneDefinition


class IntGene(GeneDefinition[int]):
    """Integer gene definition.
    :param int lower_bound: smallest possible value of a gene instance
    :param int upper_bound: highest possible value of a gene instance
    """

    def __init__(self, lower_bound: int, upper_bound: int):
        """"""
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def generate(self) -> int:
        return random.randint(self.lower_bound, self.upper_bound)


class FloatGene(GeneDefinition[float]):
    """Float gene definition.
    :param float lower_bound: smallest possible value of a gene instance
    :param float upper_bound: highest possible value of a gene instance
    """

    def __init__(self, lower_bound: float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def generate(self) -> float:
        return random.uniform(self.lower_bound, self.upper_bound)


class CharGene(GeneDefinition[str]):
    """Single character gene definition.
    :param str allowed_characters: string containing all values that the gene can assume (default: lowercase ascii)
    """

    def __init__(self, allowed_characters: Optional[str] = None):
        self.allowed_characters = allowed_characters or string.ascii_lowercase

    def generate(self) -> str:
        return random.choice(self.allowed_characters)


class StringGene(GeneDefinition[str]):
    """String gene definition
    :param Sequence[str] allowed_values: list of values that the gene can assume.
    """

    def __init__(self, allowed_values: Sequence[str]):
        self.allowed_values = allowed_values

    def generate(self) -> str:
        return random.choice(self.allowed_values)
