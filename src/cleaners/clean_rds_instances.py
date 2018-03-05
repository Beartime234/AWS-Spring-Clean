# clean_rds_instances.py

# Package Imports
import boto3

# Module Imports
import helpers
from botocore.exceptions import ClientError

# Cleaner Settings
RESOURCE_NAME = "RDS Instance"
WHITELIST_NAME = "rds_instances"
BOTO3_NAME = "rds"
BOTO3_LIST_FUNCTION = "describe_db_instances"


def clean_rds_instances() -> list:
    """Main ordering for cleaning rds_instances.

    Returns:
        A list of all terminated rds_instances
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    rds_client = boto3.client(BOTO3_NAME)
    rds_instances = get_rds(rds_client)
    terminated_rds_instances = delete_rds(rds_client, rds_instances)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_rds_instances)
    return terminated_rds_instances


def get_rds(rds_client) -> list:
    """Gets all the instances ids in an account.

    Args:
        rds_client: A EC2 boto3 client.

    Returns:
        A list of all InstanceIds in the account.
    """
    rds_instance_list = []
    paginator = rds_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        rds_instance_list = rds_instance_list + page["DBInstances"]
    return rds_instance_list


def delete_rds(rds_client, rds_instances) -> list:
    """Deletes all instances in the instances parameter.

    Args:
        rds_client: A RDS boto3 client.
        rds_instances: A list of instances you want deleted.

    Returns:
        A count of deleted instances
    """
    terminated_instances = []
    for instance in rds_instances:
        rds_indentifier = instance["DBInstanceIdentifier"]
        if helpers.check_in_whitelist(rds_indentifier, WHITELIST_NAME):
            continue
        try:
            deletion_response = rds_client.delete_db_instance(
                DBInstanceIdentifier=rds_indentifier,
                SkipFinalSnapshot=True
            )
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME, rds_indentifier)
            print(error_string)
            terminated_instances.append(error_string)
            continue
        terminated_instances.append(rds_indentifier)
    return terminated_instances
