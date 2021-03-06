#!usr/bin/env python3
"""AWS Clean

Usage:
  springclean.py (--profile PROFILE_NAME) [--configuration FILE] [-s --save]
  springclean.py (-h | --help)
  springclean.py (-v | --version)

Options:
  --profile             Profile name used with appropriate permissions into this AWS.
  --configuration=FILE  Location and name of configuration file. [default: src/configuration/default.json]
  -s --save             Saves the results to a file.
  -h --help             Show this screen.
  -v --version          Show version.

"""

# Package Imports
from docopt import docopt
from schema import Schema, SchemaError

# Module Imports
import helpers
import settings

# Cleaner Imports
from cleaners.clean_ec2_instances import clean_ec2_instances
from cleaners.clean_lambda_functions import clean_lambda_functions
from cleaners.clean_s3_buckets import clean_buckets
from cleaners.clean_rds_instances import clean_rds_instances
from cleaners.clean_dynamo_tables import clean_dynamo_tables
from cleaners.clean_redshift_clusters import clean_redshift_clusters
from cleaners.clean_ecs_clusters import clean_ecs_clusters
from cleaners.clean_efs import clean_efs


def main():
    regions = settings.REGIONS  # Get regions from config
    clean_results = {}
    if regions[0] == "global":  # If they want you to clean global resources
        print("Cleaning Global Resources.")
        helpers.set_session()  # Set a blank session for global resources
        clean_results["global"] = clean_account_globally()
        print("Finished Cleaning Globally.")
        regions.pop(0)
    for region in regions:
        print("Cleaning In {0}.".format(region))
        helpers.set_session(region)  # Set current region
        clean_results[region] = clean_account_regionally()  # Clean current regions resources
        print("Finished Cleaning In {0}.".format(region))
    helpers.save_results(clean_results)


def clean_account_regionally():
    """Destroys all resources which are globally available e.g. S3 IAM

    Returns:
        A dictionary of the results of the destruction for global resources
    """
    results = {
        "ec2_instances": clean_ec2_instances(),
        "rds_instances": clean_rds_instances(),
        "lambda_functions": clean_lambda_functions(),
        "dynamo_tables": clean_dynamo_tables(),
        "redshift_clusters": clean_redshift_clusters(),
        "ecs_clusters": clean_ecs_clusters(),
        "efs": clean_efs()
    }
    return results


def clean_account_globally():
    """Destroys all resources which are specified by region e.g. instances

    Returns:
        A dictionary of the results of the destruction for region specific resources
    """
    results = {
        "s3_buckets": clean_buckets()
    }
    return results


def validate_arguments():
    """Uses the Schema package to validate arguments

    https://pypi.python.org/pypi/schema

    Returns:
        None. Will raise an exception Schema error and show validation error.
    """
    schema = Schema({
    }, ignore_extra_keys=True)
    try:
        schema.validate(helpers.ARGUMENTS)
    except SchemaError as e:
        print(e)
        exit(1)
    return


if __name__ == '__main__':
    helpers.ARGUMENTS = docopt(__doc__, version='AWS Clean Unreleased')
    validate_arguments()
    main()
