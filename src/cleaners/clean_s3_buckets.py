# clean_s3_buckets.py

# Package Imports
import boto3
from botocore.exceptions import ClientError

# Module Imports
import helpers

# Cleaner Settings
RESOURCE_NAME = "S3 Bucket"
WHITELIST_NAME = "s3_buckets"
BOTO3_NAME = "s3"
BOTO3_LIST_FUNCTION = "" # Not used here as we use the resource method currently

def clean_buckets() -> list:
    """Main ordering for cleaning s3 buckets.

    Returns:
        A list of all terminated buckets
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    s3_client = boto3.client(BOTO3_NAME)
    buckets = get_buckets(s3_client)
    terminated_items = delete_buckets(buckets)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_items)
    return terminated_items


def get_buckets(s3_client) -> list:
    """Get all buckets in an account

    Args:
        s3_client (boto3.client): A s3 client

    Returns:
        A list of buckets
    """
    response = s3_client.list_buckets()
    buckets = response["Buckets"]  # TODO change this to the template type with pagnation
    return buckets


def delete_buckets(buckets) -> list:
    """Deletes all buckets from a list

    Args:
        buckets (list): A list of s3 buckets

    Returns:
        A list of terminated buckets
    """
    terminated_buckets = []
    for bucket in buckets:
        bucket_name = bucket["Name"]
        if helpers.check_in_whitelist(bucket_name, WHITELIST_NAME, is_global=True):
            continue
        s3 = boto3.resource(BOTO3_NAME)
        bucket = s3.Bucket(bucket_name)
        try:
            bucket.objects.all().delete() # Delete the content of the bucket
            bucket.delete()  # Delete the bucket itself
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME,
                                                     bucket_name)
            print(error_string)
            terminated_buckets.append(error_string)
        terminated_buckets.append(bucket_name)
    return terminated_buckets


