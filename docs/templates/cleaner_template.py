#
#  USE THIS TEMPLATE WHEN CREATING A NEW CLEANER
#

# cleaner_template.py

# Package Imports
import boto3

# Module Imports
import helpers
from botocore.exceptions import ClientError

# Cleaner Settings
RESOURCE_NAME = ""  # Not plural
WHITELIST_NAME = ""
BOTO3_NAME = ""
BOTO3_LIST_FUNCTION = ""


def clean_resource() -> list:
    """Main ordering for cleaning resources.

    Returns:
        A list of all terminated resources
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    resource_client = boto3.client(BOTO3_NAME)
    resources = get_resources(resource_client)
    terminated_items = delete_resources(resource_client, resources)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_items)
    return terminated_items


def get_resources(resource_client) -> list:
    """Get all resources in an account

    Args:
        resource_client (boto3.client): A resource client

    Returns:
        A list of resources
    """
    resource_list = []
    paginator = resource_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        # Your going to have to look through the response and append the correct value to the list
        resource = page["something"]
        resource_list = resource_list + resource
    return resource_list


def delete_resources(resource_client, resource_list) -> list:
    """Deletes all resources from a list

    Args:
        resource_client (boto3.Client): A boto3 client for the resource
        resource_list (list): A list of resources

    Returns:
        A list of terminated resources
    """
    terminated_resources = []
    for resource in resource_list:
        resource_actual_name = resource["ResourceName"] # Get the name used for the deletion here.
        if helpers.check_in_whitelist(resource_actual_name, WHITELIST_NAME):
            continue
        try:
            resource_client.delete_function(
                FunctionName=resource_actual_name
            )
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME,
                                                     resource_actual_name)
            print(error_string)
            terminated_resources.append(error_string)
            continue
        terminated_resources.append(resource_actual_name)
    return terminated_resources


