#settings.py

import boto3
import botocore
import json
import sys
import pathlib
import os

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

def get_from_config() -> dict:
    """Returns a the config file as a dictionary

    Returns:
        A dictionary for the configuration file

    """
    with open(ARGUMENTS["--configuration"], 'r') as conf_file:
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
    return "{0}/{1}".format(ROOT_DIR, get_from_config()["results"]["dir"])

def get_results_filename() -> str:
    """Returns the configuration filename

    Returns:
        A string that is the results filename

    """
    return "{0}/{1}".format(get_results_dir(), get_from_config()["results"]["filename"])
