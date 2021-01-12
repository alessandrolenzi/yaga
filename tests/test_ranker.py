import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Tuple

import pytest

from bounded_async_executor import BoundedAsyncioExecutor
from evolutionary_algorithm.ranker import Ranker


def score_function(individual: Tuple[int, ...]) -> float:
    return sum(individual) / len(individual)


def test_ranker_ranks_without_executor():
    ranker = Ranker(score_function)
    pop = [(0, 0, 0), (1, 0, 1), (1, 1, 1)]
    ranker.rank(pop)
    assert ranker.ranked_population[0] == ((1, 1, 1), 1)
    assert ranker.ranked_population[1] == ((1, 0, 1), float(2) / 3)
    assert ranker.ranked_population[2] == ((0, 0, 0), 0)


def test_ranker_ranks_with_executor():
    ranker = Ranker(score_function, executor=ThreadPoolExecutor(max_workers=1))
    pop = [(0, 0, 0), (1, 0, 1), (1, 1, 1)]
    ranker.rank(pop)
    assert ranker.ranked_population[0] == ((1, 1, 1), 1)
    assert ranker.ranked_population[1] == ((1, 0, 1), float(2) / 3)
    assert ranker.ranked_population[2] == ((0, 0, 0), 0)


async def async_score_function(individual: Tuple[int, ...]) -> float:
    await asyncio.sleep(0.001)
    return score_function(individual)


@pytest.mark.asyncio
def test_ranker_ranks_with_async_executor():
    with BoundedAsyncioExecutor() as executor:
        ranker = Ranker(async_score_function, executor=executor)
        pop = [(0, 0, 0), (1, 0, 1), (1, 1, 1)]
        ranker.rank(pop)
        assert ranker.ranked_population[0] == ((1, 1, 1), 1)
        assert ranker.ranked_population[1] == ((1, 0, 1), float(2) / 3)
        assert ranker.ranked_population[2] == ((0, 0, 0), 0)
