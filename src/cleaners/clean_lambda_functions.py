# clean_lambda_functions.py

# Package Imports
import boto3
from botocore.exceptions import ClientError

# Module Imports
import helpers

# Cleaner Settings
RESOURCE_NAME = "Lambda Function"
WHITELIST_NAME = "lambda_functions"
BOTO3_NAME = "lambda"
BOTO3_LIST_FUNCTION = "list_functions"


def clean_lambda_functions() -> list:
    """Main ordering for cleaning lambda functions.

    Returns:
        A list of all terminated functions
    """
    helpers.starting_clean_print(RESOURCE_NAME)
    lambda_client = boto3.client(BOTO3_NAME)
    functions = get_functions(lambda_client)
    terminated_functions = delete_functions(lambda_client, functions)
    helpers.finished_clean_print(RESOURCE_NAME, terminated_functions)
    return terminated_functions


def get_functions(lambda_client) -> list:
    """Gets all the lambda functions in an account.

    Args:
        lambda_client: A lambda boto3 client.

    Returns:
        A list of all lambda functions in the account.
    """
    function_list = []
    paginator = lambda_client.get_paginator(BOTO3_LIST_FUNCTION)
    pages = paginator.paginate()
    for page in pages:
        function_list = function_list + page["Functions"]
    return function_list


def delete_functions(lambda_client, function_list) -> list:
    """Deletes all instances in the instances parameter.

    Args:
        lambda_client: A lambda boto3 client
        function_list: A list of instances you want deleted.

    Returns:
        A count of deleted instances
    """
    terminated_functions = []
    for lambda_function in function_list:
        function_name = lambda_function["FunctionName"]
        if helpers.check_in_whitelist(function_name, WHITELIST_NAME):
            continue
        try:
            lambda_client.delete_function(
                FunctionName=function_name
            )
        except ClientError as error:
            error_string = "{0} on {1} - {2}".format(error, RESOURCE_NAME,
                                                     function_name)
            print(error_string)
            terminated_functions.append(error_string)
            continue
        terminated_functions.append(lambda_function["FunctionName"])
    return terminated_functions
