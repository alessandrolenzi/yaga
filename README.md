# YAGA: Advanced Genetic Algorithms
Target of this library is providing a way to model more complex problems in a natural way, without having to rely to string-like representation as most of the other libraries around.
Allows for several customisation points and definition of custom operators.

## Quick start

### Binary genetic algorithm
For a classic, binary genetic algorithm, you can use the `BinaryGeneticAlgorithm` class present in `genetic_algorithm` module.
As an alternative, if you want to use generic integers, you can use `IntegerGeneticAlgorithm`, which has basically the same behaviour.
You can define your genetic algorithm as follows:
```
ga = BinaryGeneticAlgorithm(
    population_size=100,
    generations=100,
    solution_size=30, #number of bits in the solution
    crossover=OnePointCrossoverOperator, #type of crossover operator
    crossover_probability=0.8,
    selector=StochasticUniversalSampling(selection_size=20)
    mutation_probability=0.1
    elite_size=10
    )
```
This will create everything to execute an integer-based genetic algorithm. The number of generations can be set to `None`, to make the algorithm continue indefinitely.
The size of the solution represents the number of bits used to represent the problem (see `all_ones.py` for an example).

YAGA exposes 3 different crossover operators:
- `OnePointCrossoverOperator` 
- `TwoPointsCrossoverOperators`
- `UniformCrossoverOperator`


each one having different properties. When defining a crossover operator, you can define an `arity` (number of parents used to apply the configuration).
It's unlimited for the `UniformCrossoverOperator`, while it's at most 3 for the `TwoPointsCrossoverOperator` and necessarily 2 for `OnePointCrossoverOperator`.
To specify it, you can write something like `partial(UniformCrossoverOperator, arity=n)`. You can also check `find_the_string.py` for a practical example.

The selector is an implementation of a *selection* algorithm. The selection algorithm is responsible for using the score achieved by the population during the previous iteration, in order to chose which possible solutions
will survive and will hence be able to pass their genes forward.
The available ones are:
- `Tournament`
- `StochasticUniversalSampling`
- `Ranking`
- `Random`

each one of them is well known in literature and has different properties.
Finally, `mutation_probability` specifies the probability of execution of a random mutation on a selected solution, `crossover_probability` has the same behaviour for the selected crossover and `elite_size` allows to select the number of individuals that will survive unmodified (depending on their score) from one generation to another.

We're almost there! If you noticed, we talked a lot about fitness and scores. But we didn't specify how a solution would be scored.
To do so, you have to call `.initialize(score_function)` on `ga_builder` object.

The score function must be in the following format:
```
def score_function(solution: Tuple[int, ...]) -> float:
    return <my_score>
```
After `initialize`, you can:
- Specify (a part of) the initial population, through `set_initial_population`
- Add callbacks, that will be called at every iteration, through `add_callback`. Callbacks will receive an `Evolution` object through which the state of the algorithm can be inspected.


and finally, you can execute `.run()` in order to get the algorithm running!

When `run` ends, it will return an `Evolution` object, allowing to retrieve the best solution.
 
An `Evolution` object has the following properties:
- fittest (best solution found)
- fittest score (score of the best solution found)
- current_iteration (last iteration run)

And the following functions:
- `population()` allowing to iterate through the latest population
- `scored_popoulation()` allowing to see the scores of all the solutions in the latest population
- `stop()`, allowing to stop the genetic algorithm (no effect after run returns)

So to recap:
```
ga = BinaryGeneticAlgorithm(
        ...
    ).initialize(
        score_function
    )

evolution = ga.run()
print(evolution.fittest, evolution.fittest_score)
```
will give you (hopefully!) the solution to your problem.

### Using different data types
YAGA is built with flexibility in mind, so you're not limited by a numeric representation for your problem.
You can just as easily solve a problem with a string representation!

For an example of this, you can check `find_the_string.py` example.

The basic idea is that you can define the structure of a problem through an `IndividualStructure`.
An individual structure represents a factory, able to produce individuals, and will be - in general - composed by a set of genes.

For example, if you want to find a string of 10 characters, you can use a shorthand for defining my individual structure:
```
individual_structure = UniformIndividualStructure(
    (CharGene(), ) * 10
)
```

You can now define a genetic algorithm working on this as follows:

```
evolutionary_algorithm = EvolutionaryAlgorithmBuilder(
    population_size: int,
    generations: Optional[int],
    individual_structure=individual_structure
)
```
Operators can now be added with `add_operators`, which takes the operator as first argument and it's execution probability as the second.
Any number of operators can be added.
```
evolutionary_algorithm.add_operator(OnePointCrossoverOperator, 0.8)
evolutionary_algorithm.add_operator(MutationOperator, 0.1)
evolutionary_algorithm.add_operator(UniformCrossoverOperator, 0.1)
```
Then, to specify a selector:
```
evolutionary_algorithm.selector(Tournament(tournament_size=5, selection_size=10))
```
and at last, our score function, to be defined through `initialize` before calling run:
```
def score_function(solution: Tuple[str, ...]) -> int:
   return sum(i == j for i, j in zip(solution, to_find))

runner = evolutionary_algorithm.initialize(score_function)
evolution = runner.run()
```

### Examples

For now there is a limited number of examples, but they should be enough to clarify or get you started.
Under `/examples`, you can find:
- `all_ones.py`, trying to maximise the number of ones in a binary sequence
- `binary_search_tree.py`, which tries to find a binary search tree maximising the overall value present in the nodes
- `eight_queens.py`, a solution to the eight queens puzzle
- `find_the_string.py` tries to "guess" a string
- `mixed_individual_test.py`, a simple test of "guessing' a certain combination of numbers and strings.


## Contributing!

I'm not even close to where i want to be with this library.
If you want to contribute, adding tests and documentation is a great way to get aquainted: go ahead and submit a pull request if you want!
New features are really welcome as well!

