from enum import Enum

from evolutionary_algorithm.operators.multiple_individuals.crossover.one_point import \
    OnePointCrossoverOperator


class CrossoverType(Enum):
    OnePoint = OnePointCrossoverOperator
