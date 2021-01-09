"""Provides a class for tracking and managing datasets, in addition
to useful utilities.

All different types of data, as they are added, are discarded in
favor of PyArrow.

Files are stored *on disk* as parquet but when instantiated are read
and stored as feather. This could be overloaded, but definitely needs
to be considered.
https://arrow.apache.org/docs/python/parquet.html

Note that this should allow for CPU or GPU (Support for CUDA)
https://arrow.apache.org/docs/python/cuda.html

PyArrow data types
https://arrow.apache.org/docs/python/api/datatypes.html#api-types

PyArrow compute functions
https://arrow.apache.org/docs/cpp/compute.html#compute-function-list

PyArrow has built in hdfs, s3, and local fs support.
https://arrow.apache.org/docs/python/filesystems.html

PyArrow has the plasma store, which is an 'in-memory object store'
https://arrow.apache.org/docs/python/plasma.html
Note the hugepages

API
https://arrow.apache.org/docs/python/api.html
"""

import pandas as pd
import pyarrow as pa
import pyarrow.flight as fl
import numpy as np
import shutil
import uuid

from typing import (
    Any,
    Dict
)

from themodelshop.utils.data.convertors import standardize as _standardize

# https://mirai-solutions.ch/news/2020/06/11/apache-arrow-flight-tutorial/
class TicketError(Exception):
    """Raised for issues with creating or accessing tickets.

    Parameters
    ----------
    custom_message: str = None
        This is a custom message which can be overloaded as necessary.
    ticket: str = None
        This is the generated ticket number.
    """
    def __init__(self, custom_message:str = None, ticket:str=None):
        message_header = "TicketError:"
        if custom_message is None:
            custom_message = ""
        if ticket is None:
            ticket_message = ""
        else:
            ticket_message = f"Ticket: {ticket}"
        message = ('\n\t'.join(message_header,custom_message,ticket_message))
        self.ticket = ticket
        self.message = message
        super().__init__(self.message)

class FileCabinet(fl.FlightServerBase):
    """Maintains records and data for a project.

    A filing cabinet is associated with a workspace. Any workspace.
    If you don't pass a file location when this is created it
    assumes that it is in a location where it is appropriate to
    store data. It checks for and creates a '.data' folder in that
    case.

    This class is designed to ingest data and serves as a location
    for the secretary to interact with a named dataset. Consider the
    'canonical' Titanic dataset. When the project 'Classify the
    Titanic dataset' is instantiated the Secretary checks for (and
    creates if necessary) a filing cabinet to maintain records for
    the project.

    The dataset *itself* is a file in the cabinet.

    Any additional training data is also stored as a file in the
    cabinet.

    As the secretary tracks work put towards a project it files
    that work towards the project. The filing cabinet stores the
    data by writing it to an appropriate location on disk in a
    efficient manner and modifying internal datasets as appropriate
    to ensure data is not lost.

    The filing cabinet can be queried at any time by the secretary
    to pull back datasets.

    This can spin up a GRPC server.

    This can spin up a 

    TODO: Implement local, test.
    TODO: Implement a metadata method listing standardized metadata.

    Parameters
    ----------
    location: str = ".data"
        This is a string denoting the location that the filing
        cabinet should store information. This will look for Model
        Shop formatted data in that location and attempt to open all
        available files.

    address: str = "grpc://0.0.0.0:8815"
        This is a string denoting the bind address and port to use.

    dataset_metadata: Dict
        This is an optional dictionary keyed by dataset name with
        values of dataset functions coupled with optional
        parameters. Any dataset defined in this way can be accessed.
        This has a *large* degree of flexibility. This is also
        tagged with any experimental results, if appropriate. All
        datasets are defined in terms of *loading functions*.

    Methods
    -------
    __init__(location:str=None):
        Checks for file structure at location, creates if necessary,
        and plants a cabinet at that location. Writes datasets
        into that location appropriately. Checks for schema definition
        at this location and creates a default schema if not
        available.

    query(**kwargs): This overloads the standard Pandas .query().
        If no parameters are passed this will return an unfiltered
        tabular dataset of metadata from all registered objects in
        this cabinet. If kwargs are passed they are assumed to be
        filters for data matching. I.e. 'X' is a metadata element.
        If the keyword expression "X=2" is passed then the internal
        dataset of metadata is queried using Pandas DataFrame.query().
        If the feature of the metadata does not exist then a MetaDataError
        is thrown.

        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html

    put(something): This adds an item to the filing cabinet and
        ensures that the metadata matches the appropriate schema.
        This is using appropriate file or variable handling
        functions which are loaded from the file_cabinet
        utilities to allow storing an item appropriately.

    register(open=True,**kwargs): This takes the datasets identified
        by this .query(**kwargs) and changes their registration status
        to 'open'. This will throw a 'QueryTooNarrow' error if no
        datasets are identified.

    get(**kwargs): This takes the dataset identified by this
        .query(**kwargs) and services a get request by returning the
        information. This is using appropriate file or variable
        handling functions which are loaded from the file_cabinet
        utilities to allow returning an item appropriately.

    open(**kwargs): This uses appropriate handling techniques to
        read the datasets identified by this .query(**kwargs) and
        ensure they are available for get operations. This will
        throw a QueryTooNarrow error if no datasets are identified.

    close(**kwargs): This uses appropriate handling techniques to
        write the datasets identified by this .query(**kwargs) and
        ensure their open status is set to false. This will throw a
        QueryTooNarrow error if no datasets are identified.

    Returns
    -------
    file_cabinet: FileCabinet
        A filing cabinet which can be queried for information.
    """
    def __init__(
        self,
        location: str = ".data",
        address: str = "grpc://0.0.0.0:8815",
        #grpc_on: bool = False,
        name: str = None,
        **kwargs
    ):
        # TODO: Think about this, should I embed the capability to
        # turn grpc off?
        super().__init__(address, **kwargs)
        # The internal dataset should be PyArrow?
        self._data = {}
        self._metadata = {}
        # This is an identifier for this cabinet.
        self._name = name
        if name is None:
            self._uuid = uuid.uuid1()
        else:
            uuid.uuid3(uuid.NAMESPACE_DNS, self._name)

    def query(self, **kwargs: Any):
        """Retrieve filterable metadata for internal datasets.

        This is a function that will return, if no parameters are
        passed, an unfiltered dataset of dataset metadata. This can
        also be passed filter criteria in order to return tailored
        information. These are **exact** filter criteria, meaning
        that if you call:

        ```python
        file_cabinet.query(x=2,y=3)

        """
        # TODO: Change this syntax to the appropriate effect.
        # This will likely need some further work, but it will
        # work as a placeholder.
        query_str = ["f{k} == {v}" for k,v in kwargs.items()]
        return pd.DataFrame(self._metadata).query(*query_str)

    def _handle(rw:str='r',obj:Any=None):
        """Read or write a file appropriately.

        If the read/write parameter is set to read then the object is
        assumed to be a string and this will then attempt to pull that
        item.

        Parameters
        ----------
        rw: str = 'r'
            'r': Read
            'w': Write
            'd': Delete
        """
        pass
    def _put(self,data):
        """Files a thing into the cabinet.

        This will place an item into storage and will return the
        necessary metadata to retrieve the data upon request.
        """
        # Generate a unique identifier for the data.
        _ticket = uuid.uuid1()
        # This will blow up if the data cannot be cast to PyArrow.
        _data = _standardize(data)
        # At this point the data is PyArrow format.
        # self.tables[ticket_name] = reader.read_all()

        return _ticket

    def _get(self):
        """Get a thing from the cabinet.

        This will get an item from storage, regardless of cabinet
        location, as long as the information is available (i.e.
        registered or available locally.)
        """
        raise NotImplementedError

    def register(self,data:Any,metadata:Dict[str,str]):
        """Register a dataset.

        This publishes an item in the cabinet, marking it as
        available. By default this will create a dissemination mask
        empty for all users aside from the current cabinet.

        Parameters
        ----------
        data: Any
            This is the object to store in the cabinet.
        metadata: Dict[str,str]
            This is a dictionary of standardized metadata fields.
            For more information call the metadata method.

        Returns
        -------
        ticket: str
            This is the unique identifier in this cabinet which is
            used to identify this dataset.
        """
        
        # Attempt to publish the data.
        ticket = self._put(data)
        try:
            self._put(data)
        try:
            self._metadata[_ticket] = metadata
            self._data[_ticket] = data
        except:
            raise TicketError("Unable to add.")

    def open(self):
        """Opens a closed cabinet.

        Opening a cabinet will check the branch workspace for a
        cabinet (if it exists in metadata already) and make available
        all information in this workspace by registering persistent
        datasets. Each filing cabinet is associated with a UUID and
        as a result cabinets can be opened and closed at will to
        allow for projects to easily be cleaned up and instantiated.
        """
        raise NotImplementedError

    def close(self):
        """Closes an open cabinet.

        Write all workspace specific non-temporary datasets to disk
        if required. Delete all temporary datasets in this workspace
        from metadata. Publish all persistent information to higher
        level cabinets, if that information is in use elsewhere.
        """
        raise NotImplementedError


def main():
    FileCabinet().serve()

if __name__ == '__main__':
    main()