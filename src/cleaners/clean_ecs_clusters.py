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
RESOURCE_NAME = "ECS Cluster"
WHITELIST_NAME = "ecs_clusters"
BOTO3_NAME = "ecs"
BOTO3_LIST_FUNCTION = "list_clusters"


def clean_ecs_clusters() -> list:
    """Main ordering for cleaning clusters.

    Returns:
        A list of all terminated clusters
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    ecs_client = boto3.client(BOTO3_NAME)
    clusters = get_ecs_clusters(ecs_client)
    terminated_clusters = delete_ecs_clusters(ecs_client, clusters)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_clusters)
    return terminated_clusters


def get_ecs_clusters(ecs_client) -> list:
    """Get all resources in an account

    Args:
        ecs_client (boto3.client): A resource client

    Returns:
        A list of clusterArns
    """
    cluster_list = []
    paginator = ecs_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        # Your going to have to look through the response and append the correct value to the list
        cluster_arns = page["clusterArns"]
        cluster_list = cluster_list + cluster_arns
    return cluster_list


def delete_ecs_clusters(cluster_client, cluster_list) -> list:
    """Deletes all resources from a list

    Args:
        cluster_client: A ecs boto3 client
        cluster_list (list): A list of resources

    Returns:
        A list of terminated resources
    """
    terminated_clusters = []
    for cluster in cluster_list:
        cluster_arn = cluster # Get the name used for the deletion here.
        if helpers.check_in_whitelist(cluster_arn, WHITELIST_NAME):
            continue
        try:
            cluster_client.delete_cluster(
                cluster=cluster_arn
            )
        except ClientError as error:
             terminated_clusters.append("{0} on {1} - {2}"
                                         "".format(error, RESOURCE_NAME, cluster_arn))
        terminated_clusters.append(cluster_arn)
    return terminated_clusters


