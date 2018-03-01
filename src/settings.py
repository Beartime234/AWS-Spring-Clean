#settings.py

import boto3
import botocore
import json
import sys

# Project Global Variables
account_session = None
arguments = {}

def set_session(region=None):
    """Sets the global _account_session variable for boto3 to the profile specified.

    Args:
        region: The region on which to switch too

    Returns:
        None

    """
    global account_session
    try:
        if region is None:
            boto3.setup_default_session(profile_name=arguments["PROFILE_NAME"])
        else:
            boto3.setup_default_session(profile_name=arguments["PROFILE_NAME"], region_name=region)
    except botocore.exceptions.ProfileNotFound:
        print("AWS Profile {0} could not be found."
              " Run aws configure --profile PROFILE_NAME".format(arguments["PROFILE_NAME"]))
        sys.exit(1)
    return

def get_from_config() -> dict:
    """Returns a the config file as a dictionary

    Returns:
        A dictionary for the configuration file

    """
    with open(arguments["--configuration"], 'r') as conf_file:
        return json.loads(conf_file.read())

def get_regions() -> list:
    """Returns the regions to delete resources from the configuration file

    Returns:
        A list of regions.

    """
    return get_from_config()["regions"]

def get_results_dir() -> str:
    """Returns the configuration directory

    Returns:
        A string that is the results directory

    """
    return get_from_config()["results"]["dir"]

def get_results_filename() -> str:
    """Returns the configuration filename

    Returns:
        A string that is the results filename

    """
    return "{0}/{1}".format(get_results_dir(), get_from_config()["results"]["filename"])
