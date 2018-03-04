#
#  USE THIS TEMPLATE WHEN CREATING A NEW CLEANER
#

# cleaner_template.py

# Package Imports
import boto3

# Module Imports
import helpers

# Cleaner Settings
RESOURCE_NAME = ""
WHITELIST_NAME = ""
BOTO3_NAME = ""


def clean_resource() -> list:
    """Main ordering for cleaning resources.

    Returns:
        A list of all terminated resources
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    resource_client = boto3.client(BOTO3_NAME)
    buckets = get_resoources(resource_client)
    terminated_items = delete_resources(resource_client, buckets)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_items)
    return terminated_items


def get_resoources(resource_client) -> list:
    """Get all resources in an account

    Args:
        resource_client (boto3.client): A resource client

    Returns:
        A list of resources
    """
    resource_list = []
    paginator = resource_client.get_paginator("list_resource")
    pages = paginator.paginate()
    for page in pages:
        for resource in page["resource_name"]:
            resource_list = resource_list + resource["resource_name"]
    return resource_list


def delete_resources(resource_client, resource_list) -> list:
    """Deletes all resources from a list

    Args:
        resource_list (list): A list of resources

    Returns:
        A list of terminated resources
    """
    terminated_resources = []
    for resource in resource_list:
        function_name = resource["ResourceName"]
        if helpers.check_in_whitelist(function_name, WHITELIST_NAME):
            continue
        resource_client.delete_function(
            FunctionName=function_name
        )
        terminated_resources.append(resource["ResourceName"])
    return terminated_resources


