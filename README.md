# The Model Shop

What is this? This is an algorithm which will, given an input set of n variables, train a team of data scientists to solve your problem.

The way it accomplishes this is by constructing a Company, which is a construct of multiple, independent, and cooperating (to a point) agents, which include:

* The Manager: The primary agent, which maintains a pool of employees.
* The Employees: Statistical modelers and learning algorithms.
* The Worker Pool: A pool of employees which share communal data networks and a company store
* The Secretary: Maintains paperwork on employees.
* The Company Store: A construct that maintains the Market.
* The Market: A storefront where the modeling employees may purchase from the variables within the target dataset.

## The Manager

The manager reviews contracts and hires skilled labor from the workforce. The manager is given a budget that is capable of maintaining a fixed number of employees ($m$) that will fill a labor pool ($M$).

When presented with your problem the manager will hire in one of two ways. It will either hire randomly or will conduct a series of experiments on its own to produce an initial educated guess as to a start point for modeling. At that point the manager will use its educated guess to hire intelligently.

### Wages

The manager will approach each agent it desires in the labor pool and will offer them a salary of wages ($w$) that is inversely proportionate to how capable they are at minimizing Mean Squared Percentile Loss.

### Harmonic Percentile Error (HPE)

TODO: Come back to this and write formulas down, but this needs to be mean squared percentile error.

The target $Y$ is either a discrete variable of the form $(y_0,y_1,\cdots,y_n)$ or a continuous variable in the range $(y_{min},y_{max})$; HPE for a categorical predictor is measured as the harmonic mean of the classification accuracy rates of the different classes ($MSPL = \frac{n}{\sum_{=1}^n \frac{1}{A_i}}$ where $A_i = \frac{\sum_{j=1}^m Y_{i_j}-\hat{Y_{i_j}}}{m}$ and $m$ is the number of observations in that class.)

For a continuous variable the same concept is applied but the buckets the data are split into are *percentile* buckets.

All models are measured against random, weighted, samples in the dataset such that samples are uniformly distributed across the percentiles of the data. All models are scored on bootstrapped samples of the testing data to produce an estimate of their performance.

### Firing Employees

When a modeler finishes their contract the manager fires the modeler on the spot and a number of copies ($W_r$) of that agent are added to the worker pool. The final MSPE for each agent is carried forward with all their copies, along with a random integer.

## The Worker Pool

The worker pool $M$ has $n_m$ potential agents in it storing their statistics; each agent stores the MSPE of its progenitor model and a random integer which is passed to a fuzzing algorithm if that agent is hired. During each hiring activity modelers are drawn from a softmax distributional function of the MSPE of the agents. When an agent leaves the pool it gains a 'personality' by running through a 'fuzzing' algorithm which inserts noise into the weights of the original agent architecture.

## The Secretary

The Secretary maintains paperwork for all agents, including which agents were hired, what variables they purchased and in what order. The Secretary can be queried for information at any time and, in addition, can provide running statistics.

## The Company Store

The company store maintains the store front from which the Modelers are allowed to purchase data. The prices for each variable are a function of:

* The recent mean loss differential estimate for this variable.
* The recent mean model complexity seen when this variable is included in the function approximator.
* The recent frequency of this variable in the last 1000 models run.

All these statistics are calculated for all variables from the last 1000 models run, which are stored in a communally accessible data structure.

Overall the effect is that variables which are predictive are cheap. Variables which haven't been touched in awhile are cheap. Variables which contribute to simpler models are cheap.

### Recent Mean Loss Differential

For a set of `n` previous most recent models which included this variable and a random sample of `m` most recent models which did not include this variable this is the difference between the normalized means of the sample subsets as $MLD = \frac{\bar{X}-\bar{Y}}{{MLD_R}_{max}}$ where $X$ is the set which did not include the variable, $Y$ is the set which did, and $MLD_R$ is the maximum value of the running loss distribution. This is maintained in such a way that the agent is maintaining a running estimate with a few parameters.

This is initially set for all n variables to a number drawn from a normal distribution centered at zero with variance 1.

The smaller the proportion of recent values within the data the higher the likelihood of instead pulling the absolute value of a random number centered at zero with variance 1.

The probability of drawning a random number is $p = e^{-n \alpha}$ where $n$ is the number of models within the buffer which used this variable and $\alpha$ is a regularization parameter which governs a desire for exploration. By default $\alpha = 1$. Setting to levels below one will actively encourage further exploration while levels higher than one will actively penalize exploration. An annealing schedule would help encourage initial shallow exploration of the search space.

This is a method of introducing supervised goal seeking into the search space and ensuring a reasonable sample size across calculated statistics.

### Recent Mean Model Complexity

Complexity for a model is calculated as $n^n$ where $n$ is the number of variables in the model. This is used, additionally, in the calculation of the Modeler rewards.

This is calculated for each variable using the models in the buffer as the samples with each variable assigned the mean complexity of the buffered models which used that variable.

This is a method of penalizing complexity.

### Recent Frequency of the Variable in Modeling Space

Confidence bounds for the estimates are a function of the recent sample size of models run with this variable. To ensure that infrequently used variables are tested the prices are proportionally adjusted downward by their sparsity in the data. The price modifier for a variable's frequency is $\frac{\sum_{i=1}^n \lambda^{i} I_i}{n}$  where $I_i$ is an indicator (binary) variable denoting whether or not the variable was used in that model. In this instance i is the most recent model and n is the model furthest in the history. Setting $\lambda$ to some arbitrary constant near 0.99 suffices for sufficiently penalizing the distant past.

This has the effect of increasing the reward associated with the agent selecting infrequent actions, thereby encouraging exploration to an extent.

TODO: Get a function of these three weights, ensure they're scaled to like variance, and then shape the weights.

## The Modelers

The modelers get to run a twelve month contract where they're training models once a month. Every month they get to buy variables, train their models, then get their model scored by the manager

This environment is a k+2 dimensional structure where k is the list of statistics you wish to keep. The 2n elements are derived from combinations of all n variables in the dataset.

# MPI in Python.