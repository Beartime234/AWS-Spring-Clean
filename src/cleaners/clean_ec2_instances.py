# clean_ec2_instances.py

# Package Imports
import boto3

# Module Imports
import helpers
from botocore.exceptions import ClientError

# Cleaner Settings
RESOURCE_NAME = "EC2 Instance"
WHITELIST_NAME = "ec2_instances"
BOTO3_NAME = "ec2"
BOTO3_LIST_FUNCTION = "describe_instances"

def clean_ec2_instances() -> list:
    """Main ordering for cleaning instances.

    Returns:
        A list of all terminated instances
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    ec2_client = boto3.client(BOTO3_NAME)
    instances = get_instances(ec2_client)
    terminated_instances = delete_instances(instances)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_instances)
    return terminated_instances


def get_instances(ec2_client) -> list:
    """Gets all the instances ids in an account.

    Args:
        ec2_client: A EC2 boto3 client.

    Returns:
        A list of all InstanceIds in the account.
    """
    instance_list = []
    paginator = ec2_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        for reservation in page["Reservations"]:
            instance_list = instance_list + reservation["Instances"]
    return instance_list


def delete_instances(instances) -> list:
    """Deletes all instances in the instances parameter.

    Args:
        instances: A list of instances you want deleted.

    Returns:
        A count of deleted instances
    """
    terminated_instances = []
    for instance in instances:
        instance_id = instance["InstanceId"]
        if helpers.check_in_whitelist(instance_id, WHITELIST_NAME):
            continue
        ec2 = boto3.resource(BOTO3_NAME)
        try:
            instance = ec2.Instance(instance_id)
            instance.terminate()  # Terminate the instance
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME, instance_id)
            print(error_string)
            terminated_instances.append(error_string)
            continue
        terminated_instances.append(instance_id)
    return terminated_instances
