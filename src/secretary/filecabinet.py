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

class FileCabinet():
    """

    """
    def __init__(self):
        self._files = {}


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
