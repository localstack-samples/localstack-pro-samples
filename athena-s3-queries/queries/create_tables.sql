CREATE TABLE localstack.test_table2 (
  id VARCHAR,
  first_name VARCHAR,
  last_name VARCHAR,
  email VARCHAR,
  gender VARCHAR,
  is_active VARCHAR,
  joined_date VARCHAR
) WITH (
  format = 'CSV',
  external_location = 's3://athena-test/data/'
)
