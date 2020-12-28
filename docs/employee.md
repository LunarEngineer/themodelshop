# The Employees

These are the data scientists. They're specialized scientists, attempting to solve a single, very narrowly defined, task.

When they are created their archetype (logistic regression, random forest, deep net) is a random function drawn from a hypothesis space. This space may draw from a wide range of potential hypotheses, or a more limited subset of hypotheses.

Each of these hypothesis spaces contains a single, trainable, importance function which is updated whenever this hypothesis space is used to create a potential solution.

This function predicts the *best* variables for this hypothesis space.

The input to this function is an, initially, n length vector. This is measuring univariate correlation with the target. This input vector can be extended, near arbitrarily, by the removal of or addition to the input space, and the execution of arbitrary named analyses which stack output into this input space.

The employee is a reinforcement learning agent which is learning which variables to select for a modeling task.
