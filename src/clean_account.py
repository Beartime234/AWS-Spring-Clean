#!usr/bin/env python3
"""AWS Clean

Usage:
  clean_account.py clean (--profile PROFILE_NAME) [--configuration FILE]
  clean_account.py (-h | --help)
  clean_account.py (-v | --version)

Options:
  --profile             Profile name used with appropriate permissions into this AWS.
  --configuration=FILE  Location and name of configuration file. [default: src/configuration/default.json]
  -h --help             Show this screen.
  -v --version          Show version.

"""

#Package Imports
from docopt import docopt
from schema import Schema, Use, SchemaError
import pathlib
import json

#Module Imports
import settings

#Cleaner Imports
from cleaners.clean_ec2_instances import clean_ec2_instances
from cleaners.clean_lambda_functions import clean_lambda_functions
from cleaners.clean_s3_buckets import clean_buckets
from cleaners.clean_rds_instances import clean_rds_instances

# Global Variables
account_session = None


def main():
    print("Cleaning Global resources.")
    settings.set_session()  # Set a blank session for global resources
    clean_results = {"global": clean_account_globally()}
    print("Finished Cleaning Global Resources.")
    regions = settings.get_regions() # Get regions from config
    for region in regions:
        print("Cleaning in {0} region.".format(region))
        settings.set_session(region)  # Set current region
        clean_results[region] = clean_account_regionally()  # Clean current regions resources
        print("Finished cleaning in {0} region.".format(region))
    write_results(clean_results) # TODO make this an argument to save


def clean_account_regionally():
    """Destroys all resources which are globally available e.g. S3 IAM

    Returns:
        A dictionary of the results of the destruction for global resources
    """
    results = {
        "ec2_instances": clean_ec2_instances(),
        "rds_instances": clean_rds_instances(),
        "lambda_functions": clean_lambda_functions()
    }
    return results


def clean_account_globally():
    """Destroys all resources which are specified by region e.g. instances

    Returns:
        A dictionary of the results of the destruction for region specific resources
    """
    results = {
        "s3buckets": clean_buckets()
    }
    return results


def write_results(results):
    """Write the results to a file

    Args:
        results (dict): The dictionary of results to write to a file

    Returns:
        None
    """
    pathlib.Path(settings.get_results_dir()).mkdir(parents=True, exist_ok=True)
    with open(settings.get_results_filename(), "w") as results_file:
        results_file.write(json.dumps(results, sort_keys=True, indent=4))
    return


def validate_arguments():
    """Uses the Schema package to validate arguments

    https://pypi.python.org/pypi/schema

    Returns:
        None. Will raise an exception Schema error and show validation error.
    """
    #print(arguments)
    schema = Schema({
        "--configuration": Use(open, error='Configuration file ({0})'
                                  ' could not be opened.'.format(settings.arguments["--configuration"]))
    }, ignore_extra_keys=True)
    try:
        schema.validate(settings.arguments)
    except SchemaError as e:
        print(e)
        exit(1)
    return


if __name__ == '__main__':
    settings.arguments = docopt(__doc__, version='AWS Clean Unreleased')
    validate_arguments()
    main()
