import collections
import random
from functools import singledispatch
from typing import TypeVar, Iterable, List

T = TypeVar("T")


def reservoir_sampling(to_select: int, iterator: Iterable[T]) -> List[T]:
    selected: List[T] = []
    for position, element in enumerate(iterator):
        if position < to_select:
            selected.append(element)
        else:
            candidate_position = random.randint(0, position)
            if candidate_position < to_select:
                selected[candidate_position] = element
    return selected


@singledispatch
def random_selection(iterator: Iterable[T], number_of_elements: int) -> List[T]:
    return reservoir_sampling(number_of_elements, iterator)


@random_selection.register(collections.abc.Sequence)
def random_selection_on_bounded(sequence, number_of_elements):
    return [
        sequence[random.randrange(0, len(sequence))] for _ in range(number_of_elements)
    ]
