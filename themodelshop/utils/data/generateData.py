"""Tools to generate data

This is a series of functions and classes which can quickly generate
datasets of varying kinds.

This needs to be able to design datasets which create random numbers
of variables, with random interactions, to produce random effects
for a random number of targets.

The 'noisiness' of this algorithm needs to be another input.

This will allow for arbitrarily complex problems to be designed to allow
the agent to solve increasingly arbitrarily complex problems! Yay.

RNG documentation: https://numpy.org/doc/stable/reference/random/generator.html

Design requirements:

1. This outputs tabular data
2. This can output varying sizes of data with a datasize parameter
3. This can output varying widths of data with a width parameter
4. The mix of types is a 'random' draw from a set list of types with a 'random function' and 'arguments' parameters
5. The problem domain can be drawn from segmentation / classification,

This is going to be required to generate high quality datasets on demand.

Come back to this after the secretary work is complete.
"""
from sklearn.datasets import (
    make_classification,
    make_regression
)
from numpy.random import default_rng

class InputError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return f'Input Error, {self.message}'
        else:
            return 'Input validation error'


class DataGenerator():
    """This is a class which can generate data upon demand

    This can generate data for two problem domains:
    1. Classification / segmentation, and
    2. Regression

    Parameters
    ----------
    seed: int
        This is an integer which may be passed to enforce repeatability.
    """
    # These are the problems the generator can generate data for.
    defined_problems = [
        'classification',
        'regression'
    ]
    def __init__(
        self,
        seed: int,
        problem_domain: str
    ) -> DataGenerator:

        self.args = dict(
            seed = seed,
            problem_domain = problem_domain
        )
        self._verify_args()
        self._init_generators()
        return self

    def _verify_args(self):
        """Check and validate all input"""
        # 1) Seed
        if not isinstance(self.args['seed'],int):
            raise InputError('Seed should be type int.')
        self.seed = self.args['seed']

        # 2) Problem Domain
        if not isinstance(self.args['problem_domain'],str):
            raise InputError('The problem domain should be a string.')
        if not self.args['problem_domain'] in self.defined_problems:
            raise InputError(f'The problem domain should be in {self.defined_problems}.')

    def _init_generators(self):
        # This base rng will be used to draw any of the initial generators
        self._base_rng = default_rng(self.seed)

    def _make_classification(self):
        make_classification(
            n_samples=100,
            n_features=20,
            n_informative=2,
            n_redundant=2,
            n_repeated=0,
            n_classes=2,
            n_clusters_per_class=2,
            weights=None,
            flip_y=0.01,
            class_sep=1.0,
            hypercube=True,
            shift=0.0,
            scale=1.0,
            shuffle=True,
            random_state=None
        )
#p