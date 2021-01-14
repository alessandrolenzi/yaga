from yaga_ga.evolutionary_algorithm.selectors.ranking import Ranking


def test_ranking_selector_returns_first():
    ranked_pop = [
        ("aaa", 3),
        ("bbb", 2),
        ("ccc", 1),
    ]
    r = Ranking(selection_size=2)
    l = list(r(ranked_pop))
    assert len(l) == 2
    assert "aaa" in l
    assert "bbb" in l
