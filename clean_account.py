#!usr/bin/env python3
"""AWS Clean

Usage:
  clean_account.py clean (--profile PROFILE_NAME)
  clean_account.py (-h | --help)
  clean_account.py (-v | --version)

Options:
  --profile         Profile name used with appropriate permissions into this AWS.
  -h --help         Show this screen.
  -v --version      Show version.

"""
from docopt import docopt
import boto3
import botocore

# Global Variables
_arguments = {}
_account_session = None


def main():
    set_session()
    clean_instances()


def clean_instances():
    pass


def set_session():
    """Sets the global _account_session variable for boto3 to the profile specified.

    Returns:
        None

    """
    global _account_session
    try:
        _account_session = boto3.Session(profile_name=_arguments["PROFILE_NAME"])
    except botocore.exceptions.ProfileNotFound:
        print("AWS Profile {0} could not be found."
              " Run aws configure --profile PROFILE_NAME".format(_arguments["PROFILE"]))
    return


if __name__ == '__main__':
    _arguments = docopt(__doc__, version='AWS Clean Unreleased')
    main()
