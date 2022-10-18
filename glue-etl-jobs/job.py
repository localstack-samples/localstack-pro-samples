# Based on: https://github.com/aws-samples/aws-glue-samples/blob/master/examples/join_and_relationalize.py

import os
import sys
from awsglue.transforms import Join
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


def main():
    glueContext = GlueContext(SparkContext.getOrCreate())

    # catalog: database and table names
    db_name = "legislators"
    tbl_persons = "persons_json"
    tbl_membership = "memberships_json"
    tbl_organization = "organizations_json"

    # output s3 and temp directories
    output_history_dir = "s3://glue-sample-target/output-dir/legislator_history"
    output_lg_single_dir = "s3://glue-sample-target/output-dir/legislator_single"
    output_lg_partitioned_dir = "s3://glue-sample-target/output-dir/legislator_part"
    redshift_temp_dir = "s3://glue-sample-target/temp-dir/"

    # Create dynamic frames from the source tables
    persons = glueContext.create_dynamic_frame.from_catalog(database=db_name, table_name=tbl_persons)
    memberships = glueContext.create_dynamic_frame.from_catalog(database=db_name, table_name=tbl_membership)
    orgs = glueContext.create_dynamic_frame.from_catalog(database=db_name, table_name=tbl_organization)

    # Keep the fields we need and rename some.
    orgs = (orgs.drop_fields(['other_names', 'identifiers'])
        .rename_field('id', 'org_id').rename_field('name', 'org_name'))

    # Join the frames to create history
    l_history = Join.apply(orgs,
        Join.apply(persons, memberships, 'id', 'person_id'), 'org_id', 'organization_id'
    ).drop_fields(['person_id', 'org_id'])

    # ---- Write out the history ----

    # Write out the dynamic frame into parquet in "legislator_history" directory
    print("Writing to /legislator_history ...")
    glueContext.write_dynamic_frame.from_options(
        frame = l_history, connection_type = "s3",
        connection_options = {"path": output_history_dir}, format = "parquet")

    # Write out a single file to directory "legislator_single" - TODO enable!
    # s_history = l_history.toDF().repartition(1)
    # print("Writing to /legislator_single ...")
    # s_history.write.parquet(output_lg_single_dir)

    # Convert to data frame, write to directory "legislator_part", partitioned by Senate / House.
    print("Writing to /legislator_part, partitioned by Senate and House ...")
    l_history.toDF().write.parquet(output_lg_partitioned_dir, partitionBy=['org_name'])

    # ---- Write out to relational databases ----

    # Convert the data to flat tables
    print("Converting to flat tables ...")
    dfc = l_history.relationalize("hist_root", redshift_temp_dir)

    # Cycle through and write back to DB
    for df_name in dfc.keys():
        m_df = dfc.select(df_name)
        print("Writing to Postgres table:", df_name)
        glueContext.write_dynamic_frame.from_jdbc_conf(
            frame = m_df,
            # should be same as CONNECTION_NAME in the bash script
            catalog_connection = "glue-etl-cluster1-connection",
            connection_options = {"dbtable": df_name, "database": "test"},
            redshift_tmp_dir = redshift_temp_dir)

main()
