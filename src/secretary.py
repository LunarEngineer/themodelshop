from numpy import array as nparray


class Secretary():
    """

    The Secretary maintains paperwork for all agents, including which
    agents were hired, what variables they purchased and in what
    order. The Secretary can be queried for information at any time and, in addition, can provide running statistics.
    """
    # What is the Secretary keeping track of?
    # 1) The labor pool
    # 2) Active employees
    # 3) Employee Transaction History
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
        pass

    def fire_employee(self,employee):
        # This removes the agent
        pass

    def employee_report(self):
        # This reports statistics on the employees in the pool
        pass

    ################################################################
    # Data management
    #   1. init_papers
    #   2. file_papers
    #   3. audit_papers
    ################################################################
    def init_papers(self):
        # This is taking the dataset that's fed to the model shop.
        # It computes some initial, simple, statistics for each
        #   feature and stores all of this information in a
        #   large numpy array.
        self.filing_cabinet = nparray([])
        pass

    def file_papers(
        self,
        information
    ):
        # This stores experiment information by updating
        pass

    def audit_papers(self):
        pass