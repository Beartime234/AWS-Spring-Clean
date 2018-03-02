#helpers.py

# Package Imports
import json
import os
import pathlib
import sys
import boto3
import botocore

# Module Imports
from settings import RESULTS_DIR, RESULTS_FILENAME, WHITELIST


# Project Global Variables
ACCOUNT_SESSION = None
ARGUMENTS = {}
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def save_results(results):
    """Write the results to a file

    Args:
        results (dict): The dictionary of results to write to a file

    Returns:
        None
    """
    if ARGUMENTS["--save"]:
        pathlib.Path(get_results_dir()).mkdir(parents=True, exist_ok=True)
        with open(get_results_filename(), "w") as results_file:
            results_file.write(json.dumps(results, sort_keys=True, indent=4))
    return


def set_session(region=None):
    """Sets the global _account_session variable for boto3 to the profile specified.

    Args:
        region: The region on which to switch too

    Returns:
        None

    """
    global ACCOUNT_SESSION
    try:
        if region is None:
            boto3.setup_default_session(profile_name=ARGUMENTS["PROFILE_NAME"])
        else:
            boto3.setup_default_session(profile_name=ARGUMENTS["PROFILE_NAME"], region_name=region)
    except botocore.exceptions.ProfileNotFound:
        print("AWS Profile {0} could not be found."
              " Run aws configure --profile PROFILE_NAME".format(ARGUMENTS["PROFILE_NAME"]))
        sys.exit(1)
    return


def get_results_dir() -> str:
    """Returns the configuration directory

    Returns:
        A string that is the results directory

    """
    return "{0}/{1}".format(ROOT_DIR, RESULTS_DIR)


def get_results_filename() -> str:
    """Returns the configuration filename

    Returns:
        A string that is the results filename

    """
    return "{0}/{1}.json".format(get_results_dir(), RESULTS_FILENAME)


def check_in_whitelist(resource_id, resource_type) -> bool:
    """Checks if the resource id is in the corresponding resources whitelist for the region

    Args:
        resource_id (str): The resource id which will reside in the whitelist
        resource_type (str): The resource type e.g. s3_bucket or ec2_instance which will be in the whitelist

    Returns:
        bool True if in whitelist false if not

    """
    region = boto3._get_default_session().region_name  # Ugly hack to get current session
    if region is None:
        region = "global"
    return True if resource_id in WHITELIST[region][resource_type] else False