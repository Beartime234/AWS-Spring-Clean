#!usr/bin/env python3
"""AWS Clean

Usage:
  clean_account.py clean (--profile PROFILE_NAME) [--conf FILE]
  clean_account.py (-h | --help)
  clean_account.py (-v | --version)

Options:
  --profile         Profile name used with appropriate permissions into this AWS.
  --conf=FILE       Location and name of configuration file. [default: src/conf/default.json]
  -h --help         Show this screen.
  -v --version      Show version.

"""
import sys
from docopt import docopt
import boto3
import botocore
import json
from schema import Schema, Use, SchemaError

# Global Variables
arguments = {}
account_session = None


def main():
    regions = get_regions()
    for region in regions:
        set_session(region)
        clean_account()

def clean_account():
    clean_instances()


def clean_instances():
    """Main ordering for cleaning instances.

    Returns:
        None
    """
    ec2_client = account_session.client("ec2")
    instances = get_instances(ec2_client)
    delete_instances_count = delete_instances(ec2_client, instances)
    print("Terminated {0} Instances".format(delete_instances_count))
    return


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
    termination_count = 0
    for instance in instances:
        print("Terminating Instance: {0}".format(instance))
        termination_response = ec2_client.terminate_instances(
            InstanceIds=[instance]
        )
        new_state = termination_response["TerminatingInstances"][0]["CurrentState"]["Name"]
        old_state = termination_response["TerminatingInstances"][0]["PreviousState"]["Name"]
        if new_state == "shutting-down":
            termination_count += 1
    return termination_count


def set_session(region):
    """Sets the global _account_session variable for boto3 to the profile specified.

    Args:
        region: The region on which to

    Returns:
        None

    """
    global account_session
    try:
        account_session = boto3.Session(profile_name=arguments["PROFILE_NAME"], region_name=region)
    except botocore.exceptions.ProfileNotFound:
        print("AWS Profile {0} could not be found."
              " Run aws configure --profile PROFILE_NAME".format(arguments["PROFILE_NAME"]))
        sys.exit(1)
    return

def get_regions() -> list:
    """Returns the regions to delete resources from the configuration file

    Returns:
        A list of regions.

    """
    with open(arguments["--conf"], 'r') as conf_file:
        configuration = json.loads(conf_file.read())
    return configuration["regions"]


def validate_arguments():
    """Uses the Schema package to validate arguments

    https://pypi.python.org/pypi/schema

    Returns:
        None. Will raise an exception Schema error and show validation error.
    """
    global arguments
    #print(arguments)
    schema = Schema({
        "--conf": Use(open, error='Configuration file ({0})'
                                  ' could not be opened.'.format(arguments["--conf"]))
    }, ignore_extra_keys=True)
    try:
        schema.validate(arguments)
    except SchemaError as e:
        print(e)
        exit(1)
    return

if __name__ == '__main__':
    arguments = docopt(__doc__, version='AWS Clean Unreleased')
    validate_arguments()
    main()
