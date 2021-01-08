import asyncio

import pytest

from bounded_async_executor import BoundedAsyncioExecutor


async def my_async_function(i: int):
    await asyncio.sleep(i)
    return i ** 2


@pytest.mark.asyncio
def test_async_executor():
    with BoundedAsyncioExecutor(max_workers=6) as executor:
        iter = list(reversed([10, 11, 12, 13, 14, 15]))
        res = [i for i in executor.map(my_async_function, iter)]
        assert len(res) == len(iter)
        for orig, retr in zip(iter, res):
            assert orig ** 2 == retr
