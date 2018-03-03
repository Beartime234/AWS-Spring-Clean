# clean_dynamo_tables.py

# Package Imports
import boto3

# Module Imports
import helpers


def clean_dynamo_tables() -> list:
    """Main ordering for cleaning dynamo tables.

    Returns:
        A list of all terminated dynamo tables
    """
    print("\tCleaning Dynamo Table/s")
    dynamo_client = boto3.client("dynamodb")
    dynamo_tables = get_dynamo_tables(dynamo_client)
    terminated_dynamo_tables = delete_dynamo(dynamo_client, dynamo_tables)
    print("\tTerminated {0} Dynamo Table/s".format(len(terminated_dynamo_tables)))
    return terminated_dynamo_tables


def get_dynamo_tables(dynamo_client) -> list:
    """Gets all the dynamo db in an account.

    Args:
        dynamo_client: A dynamo db boto3 client.

    Returns:
        A list of all dynamo tables in the account.
    """
    dynamo_tables_list = []
    paginator = dynamo_client.get_paginator("list_tables")
    pages = paginator.paginate()
    for page in pages:
        dynamo_tables_list = dynamo_tables_list + page["TableNames"]
    return dynamo_tables_list


def delete_dynamo(dynamo_client, dynamo_tables) -> list:
    """Deletes all instances in the instances parameter.

    Args:
        dynamo_client: A dunamo db boto3 client.
        dynamo_tables: A list of tables you want deleted.

    Returns:
        A count of deleted tables
    """
    terminated_tables = []
    for table in dynamo_tables:
        table_name = table
        if helpers.check_in_whitelist(table_name, "dynamo_tables"):
            continue
        deletion_response = dynamo_client.delete_table(
            TableName=table_name
        )
        terminated_tables.append(table_name)
    return terminated_tables
