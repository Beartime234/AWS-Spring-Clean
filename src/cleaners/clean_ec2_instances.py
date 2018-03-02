import boto3

import helpers


def clean_ec2_instances() -> list:
    """Main ordering for cleaning instances.

    Returns:
        A list of all terminated instances
    """
    print("\tCleaning EC2 Instances")
    ec2_client = boto3.client("ec2")
    instances = get_instances(ec2_client)
    terminated_instances = delete_instances(instances)
    print("\tTerminated {0} EC2 Instance/s".format(len(terminated_instances)))
    return terminated_instances


def get_instances(ec2_client) -> list:
    """Gets all the instances ids in an account.

    Args:
        ec2_client: A EC2 boto3 client.

    Returns:
        A list of all InstanceIds in the account.
    """
    instance_list = []
    paginator = ec2_client.get_paginator("describe_instances")
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
        if helpers.check_in_whitelist(instance_id, "ec2_instances"):
            continue
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(instance_id)
        instance.terminate()  # Terminate the instance
        terminated_instances.append(instance_id)
    return terminated_instances
