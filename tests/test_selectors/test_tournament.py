from doubles import expect

from evolutionary_algorithm.selectors.tournament import Tournament


def test_tournament_selects_best():
    ranked_pop = [
        ("aaa", 3),
        ("bbb", 2),
        ("ccc", 1),
    ]
    t = Tournament(selection_size=1, tournament_size=3)
    expect(t).pick_tournament_individuals.once().and_return(ranked_pop)
    res = list(t(ranked_pop))
    assert res[0] == "aaa"


def test_tournament_selects_best_twice_if_considered():
    ranked_pop = [
        ("aaa", 3),
        ("bbb", 2),
        ("ccc", 1),
    ]
    t = Tournament(selection_size=2, tournament_size=3)
    expect(t).pick_tournament_individuals.twice().and_return(ranked_pop)
    res = list(t(ranked_pop))
    assert res[0] == "aaa"
    assert res[1] == "aaa"
