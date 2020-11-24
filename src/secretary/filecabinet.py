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
import numpy as np
import shutil

class FileCabinet():
    """Maintains records for *seen* data for a project.

    This class is designed to ingest data and serves as a location
    for the secretary to interact with a named dataset. Consider the
    'canonical' Titanic dataset. When the project 'Classify the
    Titanic dataset' is instantiated the Secretary checks for (and
    creates if necessary) a filing cabinet to maintain records for
    the project.

    As the secretary tracks work put towards a project it files
    that work towards the project. The filing cabinet stores the
    data by writing it to an appropriate location on disk in a
    efficient manner and modifying internal datasets as appropriate
    to ensure data is not lost.

    The filing cabinet can be queried at any time by the secretary
    to pull back datasets.

    Parameters
    ----------
    filepath_or_paths: str
        This is a base filepath which points to a project root
        directory. The class assumes a `.data` folder is present,
        and will create the folder if it does not exist.
    filesystem: str = ''
        The filesystem string is used to indicate which set of
        tooling should be used

    Returns
    -------
    file_cabinet: FileCabinet
        A filing cabinet which can be opened or closed
    """
    def __init__(
        self,
        filepath_or_paths: str = '',
        filesystem: str = ''
    ):
        # 1) Test the filesystem to ensure it's within the developed
        #   tooling.
        # 1) Test filepath_or_paths to determine if it *could* be a real path.
        #   create it if necessary.
        self._files = {}
        self._filepath = filepath_or_paths

    def file(self):
        raise NotImplementedError("This is a function to add a file to a cabinet.")
    def close(self):
        """Closes a filing cabinet
        Ensures that any temporary data is written, sets all
        in-memory data to None.
        """
        # 1) Archive everything
        'shutil.make_archive'
        raise NotImplementedError
    def open(self):
        'shutil.unpack_archive'
    def _destroy(self,are_you_sure:bool=False):
        """Deletes a filing cabinet
        Removes the entire filing cabinet.
        """
        if are_you_sure:
            shutil.rmtree(self._filepath)
    def cabinet_usage(self):
        shutil.disk_usage(self._filepath)


class File():
    """

    """
    def __init__(self):
        self._data = {}
    def read(self):
        return self._read()
    def _read(self):
        raise NotImplementedError("Base class: To be overloaded.")

class FileNumpy(File):
    """
    """
    def __init__(self,filepath):
        self._data['filepath'] = filepath

    def _read(self):
