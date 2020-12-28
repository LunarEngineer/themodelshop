# The Secretary

## The Beauty of Having a Secretary

I would *kill* for a secretary.

A good secretary can tie everything together.
In the real work force a *good* secretary can be a point in an information flow network that can make or break a group.
They're the point that employees can request information, managers distribute information, and outsiders may interact.

A secretary is *running* the 'day-to-day' operations of the model shop; it serves as an interface to a filing cabinet.
It abstracts some more complex data insertion and retrieval methods on a per-project basis.

It's also managing a folder structure and managing the codebase for the project. It creates a git repository and initializes a project into it.
It then reads and writes data and code and modeling objects as requested. It does this using CookieCutter to create a template for local artifacts (datasets, functions, etc...)
This file serves as both a place for development choices to be recorded in addition to a location for documentation to be collated.

Any datasets stored on disk are stored as Parquet documents, while datasets provided to the algorithms are served as Apache arrow datasets.

### Parquet

Why parquet documents? Parquet documents are more than reasonably efficient in terms of storage and contain *embedded* metadata which includes data *types* and *sizes*, making it relatively efficient in terms of data storage and retrieval.

### [Apache Arrow](https://arrow.apache.org/docs/python/)

Arrow provides a way for reading datasets which might be *quite* large!

## API

### Different APIs for Different Customers

The end-goal of the Secretary development is to have a single construct which can sit on top of a filing cabinet.
It can sit on top of an already existing filing cabinet, or it could create a new one as part of a project.

It exposes an API to query team performance results (managers love this information.)
It exposes an API to query datasets (for modelers.)
It exposes an API to query experiment results (for modelers.)

It will expose more API over time, but the intent is that the Secretary is tailorable, while the Filing Cabinet is fairly static.

### init(self, port)

This function either creates a filing cabinet, or connects to one, depending on the port.
This assumes that a filing cabinet is accessible at this location and that all communication is valid.

This also creates the developer workspace and initializes the repository.

### data(query)

This function returns the main dataset as an Apache Arrow table. It may also take queries to pre-filter the data. It can also touch other, named, datasets upon request and serve them instead, with filtering.

### hire(agent, task)

This creates an agent to solve a problem with given hyperparameters.

### fire(agent)

Remove this agent from the employee pool. Removing this agent implies that whenever this agent is queried via the secretary a 'NoResponseAvailable' object is returned unless other agents depend on this one.

When no agents depend on this one it is physically destroyed, though the metadata associated with the agent persists.

### budget(int)

Off hand thought, allow for managers to act via budget? Setting a budget for a secretary will effectively limit the options that a Secretary has.

### query(obj)

This returns a metadata dataset of employees hired by this Secretary.
This includes performance metrics on defined tasks and can be filtered.

### predict ()

This will predict an output from given input. This is predicting towards the problem domain defined for the model shop contract.
This uses the current most highly trusted agent when predicting.