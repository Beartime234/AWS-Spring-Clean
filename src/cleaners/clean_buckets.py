import boto3
import botocore


def clean_buckets() -> list:
    """Main ordering for cleaning s3 buckets.

    Returns:
        A list of all terminated buckets
    """
    print("Cleaning Buckets")
    buckets = get_buckets()
    terminated_buckets = delete_buckets(buckets)
    print("Terminated {0} Buckets".format(len(terminated_buckets)))
    return terminated_buckets


def get_buckets() -> list:
    """Get all buckets in an account

    Returns:
        A list of buckets
    """
    s3_client = boto3.client("s3")
    response = s3_client.list_buckets()
    buckets = response["Buckets"]
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
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete() # Delete the content of the bucket
        bucket.delete()  # Delete the bucket itself
        terminated_buckets.append(bucket_name)
    return terminated_buckets


