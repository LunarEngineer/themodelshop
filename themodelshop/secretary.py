import argparse
import pyarrow.flight as fl
import sys
from numpy import array as nparray
from typing import Dict

from secretary.filecabinet import FileCabinet

class Secretary():
    """

    The Secretary maintains paperwork for all agents, including which
    agents were hired, what variables they purchased and in what
    order. The Secretary can be queried for information at any time
    and, in addition, can provide running statistics.
    """
    # What is the Secretary keeping track of?
    # 1) The labor pool
    # 2) Active employees
    # 3) Employee Transaction History
    # 4) Datasets!
    def __init__(
        self,
        laborpool='default_pool',
        employees='default_employee_class',
        max_transactions=100000
    ):
        self._laborpool = laborpool
        self._employees = employees
        self._max_transactions = max_transactions
        self._transaction_history = []

    ################################################################
    # Employee management
    #   1. hire_employees
    #   2. fire_employees
    #   3. employee_report
    ################################################################

    def hire_employee(self,employee):
        # This creates an agent
        raise NotImplementedError

    def fire_employee(self,employee):
        # This removes the agent
        raise NotImplementedError

    def employee_report(self):
        # This reports statistics on the employees in the pool
        raise NotImplementedError

    ################################################################
    # Data management
    #   1. init_papers
    #   2. file_papers
    #   3. audit_employee
    ################################################################
    def init_papers(
        self,
        dataset_metadata: Dict[str,Dict[str,str]] = None
    ):
        # This is taking the dataset that's fed to the model shop.
        # It computes some initial, simple, statistics for each
        #   feature and stores all of this information in a
        #   large numpy array.
        # This is the place to bake in security.
        self._cabinet = FileCabinet(dataset_metadata=dataset_metadata)

    def get_papers(
        self,
        requested_information: Dict[str,str]
    ):
        pass
    def file_papers(
        self,
        information
    ):
        """Publishes data to the filing cabinet
        
        This takes information in and dispurses it appropriately
        depending on the intended action.

        What that *means* is that the algorithm is going to scrape
        the data utilities when appropriate to look for means and
        methods of publishing the data. If there is a 'publish_dataset'
        function available in the environment, it will choose to
        attempt to use that function along with any arguments passed
        in.

        Datasets can be pushed to the feature store in this way and
        the transformations need to be tagged appropriately such
        that specific individuals with appropriate access can change
        data upon request while still preventing a critical data
        overwrite.
        """

        raise NotImplementedError

    def audit_employee(self):
        raise NotImplementedError


def print_response(data):
    print("=== Response ===")
    print(data)
    print("================")

def get_by_ticket(args, client):
    ticket_name = args.name
    response = client.do_get(fl.Ticket(ticket_name)).read_all()
    print_response(response)

def get_by_ticket_pandas(args, client):
    ticket_name = args.name
    response = client.do_get(fl.Ticket(ticket_name)).read_pandas()
    print_response(response)


def main():
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers()

    cmd_get_by_t = subcommands.add_parser('get_by_ticket')
    cmd_get_by_t.set_defaults(action='get_by_ticket')
    cmd_get_by_t.add_argument('-n', '--name', type=str, help="Name of the ticket to fetch.")

    cmd_get_by_tp = subcommands.add_parser('get_by_ticket_pandas')
    cmd_get_by_tp.set_defaults(action='get_by_ticket_pandas')
    cmd_get_by_tp.add_argument('-n', '--name', type=str, help="Name of the ticket to fetch.")

    args = parser.parse_args()
    if not hasattr(args, 'action'):
        parser.print_help()
        sys.exit(1)

    commands = {
        'get_by_ticket': get_by_ticket,
        'get_by_ticket_pandas': get_by_ticket_pandas,
    }

    client = fl.connect("grpc://0.0.0.0:8815")

    commands[args.action](args, client)


if __name__ == '__main__':
    main()