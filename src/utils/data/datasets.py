"""This is a small module for ease of access functions to get data.

These functions are intended to provide some simple data access
tools in order to allow for quick experimentation and ease of use.
These functions will be used by the Filing Cabinet / Secretary to
provide source data to the Model Shop.

All of these functions will return PyArrow Tables.

https://datasetsearch.research.google.com/
https://medium.com/towards-artificial-intelligence/best-datasets-for-machine-learning-data-science-computer-vision-nlp-ai-c9541058cf4f

1. The titanic dataset
https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv

2. Imagenet
http://image-net.org/


3. Mimic
https://mimic.physionet.org/gettingstarted/access/
"""
import pyarrow as pa
import pyarrow.dataset as ds
from urllib.request import (
    urlretrieve,
    ContentTooShortError
)

__TITANIC_PATH__ = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'

def titanic(
    retries: int = 3,
    verbose: bool = False
):
    """Go snag the titanic dataset

    Parameters
    ----------
    retries: int = 3
        The number of attempts the function will make when trying to
        download the data. This attempts to download a CSV from the
        link defined in the module. If this is breaking, you should
        investigate whether you have access to that CSV.
    verbose: bool = False
        Return the httpmessage as well

    Returns
    -------
    tbl, (httpmessage): pyarrow.table, httpmessage
        This is the Titanic dataset, read in as a PyArrow table.
        This also has an optional httpmessage.
    """
    attempt = 1
    # This is just a blanket assignment to prevent silliness and get
    #   my linter to stop yelling at me.
    fpath, httpmsg = None, None
    while attempt < 4:
        try:
            fpath, httpmsg = urlretrieve(__TITANIC_PATH__)
            break
        except ContentTooShortError:
            fpath, httpmsg = None, None
            attempt +=1
    if fpath is None:
        errmsg = f"""Unable to download file
        {retries} number of attempts exceeded.
        """
        raise FileNotFoundError(errmsg)
    # Turn the dataset into a pyarrow table
    tbl = ds.dataset(fpath,format='csv').to_table()
    if verbose:
        return tbl, httpmsg
    else:
        return tbl
