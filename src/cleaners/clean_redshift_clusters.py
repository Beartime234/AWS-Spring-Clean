# cleaner_template.py

# Package Imports
import boto3

# Module Imports
import helpers
from botocore.exceptions import ClientError

# Cleaner Settings
RESOURCE_NAME = "Redshift Cluster"
WHITELIST_NAME = "redshift_clusters"
BOTO3_NAME = "redshift"
BOTO3_LIST_FUNCTION = "describe_clusters"

def clean_redshift_clusters() -> list:
    """Main ordering for cleaning resources.

    Returns:
        A list of all terminated resources
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    redshift_cluster = boto3.client(BOTO3_NAME)
    buckets = get_redshift_clusters(redshift_cluster)
    terminated_items = delete_redshift_clusters(redshift_cluster, buckets)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_items)
    return terminated_items


def get_redshift_clusters(redshift_client) -> list:
    """Get all resources in an account

    Args:
        redshift_client (boto3.client): A resource client

    Returns:
        A list of resources
    """
    resource_list = []
    paginator = redshift_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        resource_list = resource_list + page["Clusters"]
    return resource_list


def delete_redshift_clusters(redshift_client, cluster_list) -> list:
    """Deletes all resources from a list

    Args:
        redshift_client: A redshift cluster
        cluster_list (list): A list of resources

    Returns:
        A list of terminated resources
    """
    terminated_clusters = []
    for cluster in cluster_list:
        cluster_id = cluster["ClusterIdentifier"]
        if helpers.check_in_whitelist(cluster_id, WHITELIST_NAME):
            continue
        try:
            redshift_client.delete_cluster(
                ClusterIdentifier=cluster_id,
                SkipFinalClusterSnapshot=True  # TODO make this a option
            )
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME, cluster_id)
            print(error_string)
            terminated_clusters.append(error_string)
            continue
        terminated_clusters.append(cluster_id)
    return terminated_clusters


