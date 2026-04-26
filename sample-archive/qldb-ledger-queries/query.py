import os
import boto3
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.config.retry_config import RetryConfig

QLDB_ENDPOINT = os.environ.get('QLDB_ENDPOINT') or 'http://localhost:4566'
# Configure retry limit to 3
retry_config = RetryConfig(retry_limit=3)


def create_table(transaction_executor, table_name):
    transaction_executor.execute_statement(f"Create TABLE {table_name}")


def insert_documents(transaction_executor, table_name, arg_1):
    transaction_executor.execute_statement(f"INSERT INTO {table_name} ?", arg_1)


def create_list_tables():
    print('Scenario 1: create and list tables in ledger')
    print('-----------')
    ledger_name = create_ledger()
    print('Creating new test ledger in QLDB API: %s' % ledger_name)
    driver = get_driver(ledger_name)

    print('Creating two test tables in ledger')
    tables = list(driver.list_tables())
    assert tables == []
    driver.execute_lambda(lambda executor: create_table(executor, "foobar1"))
    driver.execute_lambda(lambda executor: create_table(executor, "foobar2"))
    tables = list(driver.list_tables())
    print('Retrieves list of tables in ledger %s: %s' % (ledger_name, tables))
    assert tables == ['foobar1', 'foobar2']
    print('-----------')


def query_join_tables():
    print('Scenario 2: create ledger tables and run join query')
    print('-----------')
    ledger_name = create_ledger()
    driver = get_driver(ledger_name)

    print('Creating two test tables in ledger - "Vehicle" and "VehicleRegistration"')

    # create tables
    driver.execute_lambda(lambda executor: create_table(executor, "Vehicle"))
    driver.execute_lambda(lambda executor: create_table(executor, "VehicleRegistration"))

    # insert data
    persons_to_vehicles = {'p1': ['v1'], 'p2': ['v2', 'v3']}
    for person, vehicles in persons_to_vehicles.items():
        for vehicle in vehicles:
            doc_1 = {"id": vehicle}
            driver.execute_lambda(lambda x: insert_documents(x, table_name="Vehicle", arg_1=doc_1))
            doc_2 = {'id': vehicle, 'Owner': {'PersonId': person}}
            driver.execute_lambda(lambda x: insert_documents(x, table_name="VehicleRegistration", arg_1=doc_2))

    # run queries
    print('Running a query that joins data from the two tables')
    query = ('SELECT Vehicle FROM Vehicle INNER JOIN VehicleRegistration AS r '
        'ON Vehicle.id = r.id WHERE r.Owner.PersonId = ?')

    # Query the table
    result = []
    for pid in persons_to_vehicles.keys():
        def read_documents(transaction_executor):
            cursor = transaction_executor.execute_statement(query, pid)
            for doc in cursor:
                result.append(convert_to_dict(doc))

        driver.execute_lambda(lambda executor: read_documents(executor))
    print('Query result: %s' % result)
    assert result == [{'Vehicle': {'id': id}} for id in ['v1', 'v2', 'v3']]


def convert_to_dict(entry):
    entry = dict(entry)
    for k, v in entry.items():
        entry[k] = dict(v)
    return entry


def create_ledger():
    client = connect_qldb()
    ledger_name = 'ledger-test-1'
    client.create_ledger(Name=ledger_name, PermissionsMode='ALLOW_ALL')
    return ledger_name


def get_driver(ledger_name):
    return QldbDriver(ledger_name=ledger_name, retry_config=retry_config, endpoint_url=QLDB_ENDPOINT)


def connect_qldb():
    return boto3.client('qldb', endpoint_url=QLDB_ENDPOINT)


def main():
    create_list_tables()
    query_join_tables()


if __name__ == '__main__':
    main()
