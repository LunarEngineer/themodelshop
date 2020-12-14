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