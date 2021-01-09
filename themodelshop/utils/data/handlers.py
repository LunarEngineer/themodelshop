"""Utilities for working with data.

These are intended to be used predominantly by the filing cabinet
in order to read and write datasets appropriately.
"""

from typing import Any

def _get_handlers(location:str=""):
    """Returns available file handlers.

    This checks for a handlers folder at this location and will
    scrape the handlers available, returning them, along with all
    the handlers in this package, as a dictionary keyed by the file
    type.

    Parameters
    ----------
    location: str = ""
        The location where *extra* handlers should be examined for.
        Note that any malformed handlers will simply be skipped.

    """

