import pytest
from themodelshop.file_cabinet import FileCabinet

@pytest.mark.unit
def test_null_init():
    # What is this going to do?
    # This is going to test the init routine
    #1) Create a file cabinet
    cabinet = FileCabinet()
    #2) Check for... stuff!
    required_attr = {
        '_get': None,
        '_put': None,
        'get': None,
        'put': None,
        'register': None,
        'query': None,
        'open': None,
        'close': None,
        'do_action': None,
        'do_exchange': None,
        'do_get': None,
        'do_put': None,
        'get_flight_info': None,
        'get_schema': None,
        'list_actions': None,
        'list_flights': None,
        'port': None,
        'run': None,
        'serve': None,
        'shutdown': None,
        'wait': None
    }
    for attr in required_attr:
        if not hasattr(cabinet,attr):
            raise AttributeError(f"Filing cabinet is missing {attr}")

def test_serve():
    cabinet = FileCabinet()