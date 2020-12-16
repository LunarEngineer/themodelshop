# The Secretary

This file serves as both a place for development choices to be recorded in addition to a location for documentation to be collated.

## The Beauty of Having a Secretary

I would *kill* for a secretary.

The secretary is a class which *manages* the datasets available, including those created by the algorithms.

Any datasets stored on disk are stored as Parquet documents, while datasets provided to the algorithms are provided as Apache arrow datasets.

### Parquet

Why parquet documents? Parquet documents are more than reasonably efficient in terms of storage and contain *embedded* metadata which includes data *types* and *sizes*, making it wonderfully efficient in terms of data storage and retrieval.

Yay!

### [Apache Arrow](https://arrow.apache.org/docs/python/)

Arrow provides a way for reading datasets which might be *quite* large!

## Different APIs for Different Customers

The end-goal of the Secretary development is to have a single construct which can sit on top of a filing cabinet.
It can sit on top of an already existing filing cabinet, or it could create a new one as part of a project.

It exposes an API to query team performance results (managers love this information.)
It exposes an API to query datasets (for modelers.)
It exposes an API to query experiment results (for modelers.)

It will expose more API over time, but the intent is that the Secretary is tailorable, while the Filing Cabinet is fairly static.