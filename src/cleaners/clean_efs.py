# clean_efs.py

# Package Imports
import boto3

# Module Imports
import helpers
from botocore.exceptions import ClientError

# Cleaner Settings
RESOURCE_NAME = "Elastic File System"  # Not plural
WHITELIST_NAME = "efs"
BOTO3_NAME = "efs"
BOTO3_LIST_FUNCTION = "describe_file_systems"


def clean_efs() -> list:
    """Main ordering for cleaning resources.

    Returns:
        A list of all terminated resources
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    efs_client = boto3.client(BOTO3_NAME)
    file_systems = get_file_systems(efs_client)
    terminated_file_systems = delete_file_systems(efs_client, file_systems)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_file_systems)
    return terminated_file_systems


def get_file_systems(efs_client) -> list:
    """Get all resources in an account

    Args:
        efs_client (boto3.client): A efs client

    Returns:
        A list of resources
    """
    file_systems_list = []
    paginator = efs_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        # Your going to have to look through the response and append the correct value to the list
        file_system = page["FileSystems"]
        file_systems_list = file_systems_list + file_system
    return file_systems_list


def delete_file_systems(efs_client, file_system_list) -> list:
    """Deletes all resources from a list

    Args:
        efs_client (boto3.Client): A boto3 client for EFS
        file_system_list (list): A list of resources

    Returns:
        A list of terminated resources
    """
    terminated_file_systems = []
    for file_system in file_system_list:
        file_system_id = file_system["FileSystemId"] # Get the name used for the deletion here.
        if helpers.check_in_whitelist(file_system_id, WHITELIST_NAME):  # TODO need to create a cleaner for the mount targets
            continue
        try:
            efs_client.delete_file_system(
                FileSystemId=file_system_id
            )
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME,
                                                     file_system_id)
            print(error_string)
            terminated_file_systems.append(error_string)
            continue
        terminated_file_systems.append(file_system_id)
    return terminated_file_systems


