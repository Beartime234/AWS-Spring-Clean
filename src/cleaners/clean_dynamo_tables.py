# clean_dynamo_tables.py

# Package Imports
import boto3

# Module Imports
import helpers
from botocore.exceptions import ClientError

# Cleaner Settings
RESOURCE_NAME = "Dynamo Table"
WHITELIST_NAME = "dynamo_tables"
BOTO3_NAME = "dynamodb"
BOTO3_LIST_FUNCTION = "list_tables"


def clean_dynamo_tables() -> list:
    """Main ordering for cleaning dynamo tables.

    Returns:
        A list of all terminated dynamo tables
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    dynamo_client = boto3.client(BOTO3_NAME)
    dynamo_tables = get_dynamo_tables(dynamo_client)
    terminated_dynamo_tables = delete_dynamo(dynamo_client, dynamo_tables)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_dynamo_tables)
    return terminated_dynamo_tables


def get_dynamo_tables(dynamo_client) -> list:
    """Gets all the dynamo db in an account.

    Args:
        dynamo_client: A dynamo db boto3 client.

    Returns:
        A list of all dynamo tables in the account.
    """
    dynamo_tables_list = []
    paginator = dynamo_client.get_paginator(BOTO3_LIST_FUNCTION)
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
        if helpers.check_in_whitelist(table_name, WHITELIST_NAME):
            continue
        try:
            deletion_response = dynamo_client.delete_table(
                TableName=table_name
            )
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME, table_name)
            print(error_string)
            terminated_tables.append(error_string)
            continue
        terminated_tables.append(table_name)
    return terminated_tables
