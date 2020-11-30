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

import pyarrow as pa
import pyarrow.flight as fl
import numpy as np
import shutil

from typing import (
    Any,
    Dict
)

# https://mirai-solutions.ch/news/2020/06/11/apache-arrow-flight-tutorial/

# class File():
#     """

#     """
#     def __init__(self):
#         self._data = {}
#         #pq.read_table("s3://my-bucket/data.parquet")
#     def read(self):
#         return self._read()
#     def _read(self):
#         raise NotImplementedError("Base class: To be overloaded.")


# class FileNumpy(File):
#     """
#     """
#     def __init__(self,filepath):
#         self._data['filepath'] = filepath

#     def _read(self):
#         raise NotImplementedError



class FileCabinet(fl.FlightServerBase):
    """Maintains records for *seen* data for a project.

    This class is designed to ingest data and serves as a location
    for the secretary to interact with a named dataset. Consider the
    'canonical' Titanic dataset. When the project 'Classify the
    Titanic dataset' is instantiated the Secretary checks for (and
    creates if necessary) a filing cabinet to maintain records for
    the project.

    The dataset *itself* is also a file in the cabinet.

    Any additional training data is also stored as a file in the
    cabinet.

    As the secretary tracks work put towards a project it files
    that work towards the project. The filing cabinet stores the
    data by writing it to an appropriate location on disk in a
    efficient manner and modifying internal datasets as appropriate
    to ensure data is not lost.

    The filing cabinet can be queried at any time by the secretary
    to pull back datasets.

    Parameters
    ----------
    location: str = "grpc://0.0.0.0:8815"
        This is a string telling the file cabinet where to look
        for data. You can choose to instantiate this with the local
        host *or* could connect to a persistent server.

    dataset_metadata: Dict
        This is an optional dictionary keyed by dataset name with
        values of dataset functions coupled with optional
        parameters. Any dataset defined in this way can be accessed.
        This has a *large* degree of flexibility. This is also
        tagged with any experimental results, if appropriate. All
        datasets are defined in terms of *loading functions*.

    Returns
    -------
    file_cabinet: FileCabinet
        A filing cabinet which can be queried for information.
    """
    def __init__(
        self,
        location: str = "grpc://0.0.0.0:8815",
        dataset_metadata: Dict[str,Dict[str,str]] = None,
        **kwargs
    ):
        super(FileCabinet, self).__init__(location, **kwargs)
        # This is going to get populated by the metadata, if passed.
        self._named_datasets = {}
        if dataset_metadata is not None:
            self._build_database(dataset_metadata)

    def _build_database(
        self,
        metadata: Dict[str,Dict[str,Any]]
    ):
        """Builds appropriate data access functions for named data

        This operates similarly to a feature store. You define a
        named dataset, or a connection to something which populates
        named datasets, and this will construct the internal data
        access mechanisms to allow touching those datasets.

        Parameters
        ----------
        metadata: Dict[str,Dict[str,Any]]
            This is a dictionary, keyed by dataset name, with values
            of dictionaries expecting to see a few key parameters.
            An example of this would be:

            ```python
            project_datasets = {
                'specific_raw_data': {
                    'loading_function': 'get_sql',
                    'function_arguments': {
                        'sql_string': 'Silly arbitrary select statements'
                    }
                },
                'some_transformed_data': {
                    'loading_function': 'get_s3',
                    'function_arguments': {
                        's3_path': 's3://bucket/with/prefix'
                    }
                }
            }
            ```
        """
        # We're going to add the datasets to the internal store, one
        #   at a time.
        for named_dataset in metadata.keys():
            _loading_function = metadata[named_dataset]['loading_function']
            _loading_function_arguments = metadata[named_dataset]['function_arguments']
            _hook = self._scrape_hook(_loading_function,_loading_function_arguments)
            self._named_datasets[named_dataset] = _hook
        

    def _scrape_hook(
        function_name: str,
        function_kwargs: Dict[str,Any]
    ):
        # TODO: Use inspect to scrape functions from named user modules.
        function = None
        # Get that function and return it as a lambda function.
        raise NotImplementedError

    def do_get(self, context, ticket):
        """Fetch a dataset

        Parameters
        ----------
        context: unknown
        ticket: unknown
        """
        table = self.tables[ticket.ticket]
        return fl.RecordBatchStream(table)
    def _get():
        pass
    def _put():
        pass

    # def file(self):
    #     silly_file_name = ''
    #     self._files[silly_file_name] = File()

    # def close(self):
    #     """Closes a filing cabinet
    #     Ensures that any temporary data is written, sets all
    #     in-memory data to None.
    #     """
    #     # 1) Archive everything
    #     'shutil.make_archive'
    #     raise NotImplementedError
    # def open(self):
    #     'shutil.unpack_archive'
    # def _destroy(self,are_you_sure:bool=False):
    #     """Deletes a filing cabinet
    #     Removes the entire filing cabinet.
    #     """
    #     if are_you_sure:
    #         shutil.rmtree(self._filepath)
    # def cabinet_usage(self):
    #     shutil.disk_usage(self._filepath)

def main():
    FileCabinet().serve()

if __name__ == '__main__':
    main()