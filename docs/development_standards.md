# Development Standards

This will be a place to collate any off-topic development standards until such time as they have a useful place to be stored.

## Development in containers

This is going to be complex enough that this *will be developed and shipped* in a container.

Everything will be open source.

## Python class variables and methods.

All class variables used *only* by the classes shall be prefaced with a '_' to indicate that they're private.

That goes for methods as well.

## Testing

Before elements of the agent can be committed to master they *must* pass bandit, flake8, mypy, and have 100% code coverage.

## Atomicity

Strive for, as much as possible, classes which have atomic tasks (though possibly complex.) Try not to overlap functionality.

## Documentation

No one gets off with bad documentation. Any documentation added to the repo must pass muster after being examined by multiple people.