from doubles import expect

from evolutionary_programming.selectors.random import Random


def test_random_selector():
    r = Random(selection_size=2)
    expect(r).make_unique_indexes.once().and_return({0, 2})
    ranked_pop = [
        ("aaa", 1),
        ("bbb", 2),
        ("ccc", 3),
    ]
    l = list(r(ranked_pop))
    assert len(l) == 2
    assert "aaa" in l
    assert "ccc" in l
