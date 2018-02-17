import boto3
import botocore


def clean_instances() -> list:
    """Main ordering for cleaning instances.

    Returns:
        A list of all terminated instances
    """
    print("Cleaning Instances")
    ec2_client = boto3.client("ec2")
    instances = get_instances(ec2_client)
    terminated_instances = delete_instances(ec2_client, instances)
    print("Terminated {0} Instances".format(len(terminated_instances)))
    return terminated_instances


def get_instances(ec2_client) -> list:
    """Gets all the instances ids in an account.

    Args:
        ec2_client: A EC2 boto3 client.

    Returns:
        A list of all InstanceIds in the account.
    """
    instance_list = []
    response = ec2_client.describe_instances()
    for reservation in response["Reservations"]:
        for instances in reservation["Instances"]:
            instance_list.append(instances["InstanceId"])
    return instance_list


def delete_instances(ec2_client, instances):
    """Deletes all instances in the instances parameter.

    Args:
        ec2_client: A EC2 boto3 client.
        instances: A list of instances you want deleted.

    Returns:
        A count of deleted instances
    """
    terminated_instances = []
    for instance_id in instances:
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(instance_id)
        instance.terminate()  # Terminate the instance
        terminated_instances.append(instance_id)
    return terminated_instances