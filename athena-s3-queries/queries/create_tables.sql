-- Hive DDL format:
CREATE EXTERNAL TABLE test_db.test_table1 (
  id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  gender STRING,
  is_active BOOLEAN,
  joined_date STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3a://athena-test/data/'


-- Presto DDL format:
-- CREATE TABLE hive.test_table1 (
--   id VARCHAR,
--   first_name VARCHAR,
--   last_name VARCHAR,
--   email VARCHAR,
--   gender VARCHAR,
--   is_active VARCHAR,
--   joined_date VARCHAR
-- ) WITH (
--   format = 'CSV',
--   external_location = 's3://athena-test/data/'
-- )
