import random
import string
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

GeneType = TypeVar('GeneType')

class GeneDefinition(Generic[GeneType], ABC):
    @abstractmethod
    def generate(self) -> GeneType:
        pass


class IntGene(GeneDefinition[int]):
    def __init__(self, lower_bound: int, upper_bound: int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def generate(self) -> int:
        return random.randint(self.lower_bound, self.upper_bound)


class FloatGene(GeneDefinition[float]):
    def __init__(self, lower_bound: float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def generate(self) -> float:
        return random.uniform(self.lower_bound, self.upper_bound)


class CharGene(GeneDefinition[str]):
    def __init__(self, allowed_characters: Optional[str] = None):
        self.allowed_characters = allowed_characters or string.ascii_lowercase

    def generate(self) -> str:
        return random.choice(self.allowed_characters)

