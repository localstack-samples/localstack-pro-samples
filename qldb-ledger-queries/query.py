import os
import boto3
from pyqldb.driver.pooled_qldb_driver import PooledQldbDriver

QLDB_ENDPOINT = os.environ.get('QLDB_ENDPOINT') or 'http://localhost:4566'


def create_list_tables():
    print('Scenario 1: create and list tables in ledger')
    print('-----------')
    ledger_name = create_ledger()
    print('Creating new test ledger in QLDB API: %s' % ledger_name)
    driver = get_driver(ledger_name)
    session = driver.get_session()

    print('Creating two test tables in ledger')
    tables = list(session.list_tables())
    assert tables == []
    session.execute_statement('CREATE TABLE foobar1')
    session.execute_statement('CREATE TABLE foobar2')
    tables = list(session.list_tables())
    tables = [t.text for t in tables]
    print('Retrieves list of tables in ledger %s: %s' % (ledger_name, tables))
    assert tables == ['foobar1', 'foobar2']
    print('-----------')


def query_join_tables():
    print('Scenario 2: create ledger tables and run join query')
    print('-----------')
    ledger_name = create_ledger()
    driver = get_driver(ledger_name)
    session = driver.get_session()

    print('Creating two test tables in ledger - "Vehicle" and "VehicleRegistration"')

    # create tables
    session.execute_statement('CREATE TABLE Vehicle')
    session.execute_statement('CREATE TABLE VehicleRegistration')

    # insert data
    persons_to_vehicles = {'p1': ['v1'], 'p2': ['v2', 'v3']}
    for person, vehicles in persons_to_vehicles.items():
        for vehicle in vehicles:
            session.execute_statement('INSERT INTO Vehicle ?', {'id': vehicle})
            session.execute_statement('INSERT INTO VehicleRegistration ?',
                {'id': vehicle, 'Owner': {'PersonId': person}})

    # run queries
    print('Running a query that joins data from the two tables')
    query = ('SELECT Vehicle FROM Vehicle INNER JOIN VehicleRegistration AS r '
        'ON Vehicle.id = r.id WHERE r.Owner.PersonId = ?')

    result = []
    for pid in persons_to_vehicles.keys():
        cursor = session.execute_statement(query, pid)
        for entry in cursor:
            result.append(convert_to_dict(entry))
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
    return PooledQldbDriver(ledger_name=ledger_name, endpoint_url=QLDB_ENDPOINT)


def connect_qldb():
    return boto3.client('qldb', endpoint_url=QLDB_ENDPOINT)


def main():
    create_list_tables()
    query_join_tables()


if __name__ == '__main__':
    main()
