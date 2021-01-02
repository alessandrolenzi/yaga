from doubles import expect

from evolutionary_programming.selectors.stochastic_universal_sampling import (
    StochasticUniversalSampling,
)


def test_sus_retrieves_right_number_of_individuals():
    ranked_pop = [("aaa", 1), ("bbb", 2), ("ccc", 3), ("ddd", 4)]
    s = StochasticUniversalSampling(selection_size=2)
    assert len(list(s(ranked_pop))) == 2


def test_sus_selects_indicated_points():
    ranked_pop = [
        ("aaa", 3),
        ("ccc", 2),
        ("ddd", 1),
    ]
    s = StochasticUniversalSampling(selection_size=2)
    expect(s).make_selection_points.once().and_return([2.8, 5.4])
    retrieved = list(s(ranked_pop))
    assert "aaa" in retrieved
    assert "ddd" in retrieved


def test_sus_selects_multiple_times():
    ranked_pop = [
        ("aaa", 3),
        ("ccc", 2),
        ("ddd", 1),
    ]
    s = StochasticUniversalSampling(selection_size=2)
    expect(s).make_selection_points.once().and_return([2, 2.8])
    retrieved = list(s(ranked_pop))
    assert "aaa" in retrieved
    assert len(retrieved) == 2
