import http
import pyarrow as pa
import pytest
from themodelshop.utils.data import datasets as ds

@pytest.mark.parameterize
def test_titanic():
    # Go get the data
    tit_tbl, msg = ds.titanic(retries=1,verbose=True)
    # Check the dataset
    if not isinstance(tit_tbl,pa.Table):
        raise TypeError("Titanic: Table not PyArrow Table")
    if set(tit_tbl.column_names).isdisjoint(
        [
            'Survived',
            'Pclass',
            'Name',
            'Sex',
            'Age',
            'Siblings/Spouses Aboard',
            'Parents/Children Aboard',
            'Fare'
        ]
    ):
        raise KeyError("Titanic: Dataset columns don't match")
    if tit_tbl.nbytes != 76317:
        raise MemoryError(f"Titanic: Expected 76317 bytes and received {tit_tbl.nbytes}")
    # Check the Http message
    if not isinstance(msg,http.client.HTTPMessage):
        raise("Titanic: Verbose message not HTTPMessage")
    # TODO: Think about adding some more error checking for the httpmessage.

