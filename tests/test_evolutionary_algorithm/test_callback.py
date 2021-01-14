from yaga_ga.evolutionary_algorithm.evolution import Evolution


def test_callback_can_stop_evolution(default_evolutionary_algorithm):
    last_iteration = 0

    def callback(evolution: Evolution):
        nonlocal last_iteration
        evolution.stop()
        last_iteration = evolution.current_iteration

    default_evolutionary_algorithm._iterations_callback.append(callback)
    default_evolutionary_algorithm.run()
    assert last_iteration == 1


def test_callback_can_find_best_individual(default_evolutionary_algorithm):
    called = False

    def callback(evolution: Evolution):
        nonlocal called
        best = max(evolution.scored_population, key=lambda x: x[1])
        assert best[0] == evolution.fittest
        assert best[1] == evolution.fittest_score
        called = True

    default_evolutionary_algorithm._iterations_callback.append(callback)
    default_evolutionary_algorithm.run()
    assert called


def test_callback_retrieves_right_population(default_evolutionary_algorithm):
    initial_population = [
        (1, 0, 1, 0, 1, 0, 1, 0, 1, 0)
    ] * default_evolutionary_algorithm.generations
    called = False

    def callback(evolution: Evolution):
        nonlocal called
        assert list(evolution.population) == initial_population
        evolution.stop()
        called = True

    default_evolutionary_algorithm._iterations_callback.append(callback)
    default_evolutionary_algorithm.set_initial_population(initial_population)

    default_evolutionary_algorithm.run()
    assert called


def test_callback_return_correctly_ranked_population(default_evolutionary_algorithm):
    initial_population = [
        (1, 0, 1, 0, 1, 0, 1, 0, 1, 0)
    ] * default_evolutionary_algorithm.generations
    called = False

    def callback(evolution: Evolution):
        nonlocal called
        assert list(evolution.scored_population) == [
            (individual, float(sum(individual)) / len(individual))
            for individual in initial_population
        ]
        evolution.stop()
        called = True

    default_evolutionary_algorithm._iterations_callback.append(callback)
    default_evolutionary_algorithm.set_initial_population(initial_population)

    default_evolutionary_algorithm.run()
    assert called
