# Filing Cabinets

What's the point behind having a filing cabinet?

The filing cabinet is a *feature store* which is retaining data, metrics, and more.
What that really *means* is that when you spin up a Filing Cabinet you spin up a class which presents a standardized API for querying data.
Filing cabinets can be remote or local and can be queried for:

* Experiment results,
* Data,
* Project Artifacts, and
* More.

If you already *have* a Filing Cabinet running (either remotely or locally), and simply want to present an API for allowing trusted agents to connect, this is intended to allow for that.

This is an on-demand workspace that can be created fresh, or wrap an existing workspace and query it for information. The API is identical, simply requiring a passed port mapping when you create the object.

These workspaces store data, functions, and more by using PyArrow and Flight. This allows for easily distributed data and computation while losing little in terms of information availability.

Whenever an item is added to a filing cabinet it is registered with the cabinet and becomes queriable, meaning that any metadata associated with objects stored is presented when queried.

All filing cabinets are associated with one primary dataset, any number of secondary datasets, a primary codebase, and any number of secondary codebases.

A filing cabinet is an 'in-memory' object store and should be housed on an appropriate node.

## API

### init(self, port)

This function either creates an Apache Flight server, or connects to one, depending on the port.

It also sets the accessors appropriately, meaning that gets and puts are invisibly different.

### query(self,ticket=None,**queryArgs)

By default, with no additional parameters passed, this returns a metadata dataset of all items available in the filing cabinet, including ticket numbers.

Passing a ticket number will, instead, retrieve

### get(ticket)

Get this object.

### put()

This registers a new object in the filing cabinet.
