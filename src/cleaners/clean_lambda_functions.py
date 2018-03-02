import boto3
import botocore


def clean_lambda_functions() -> list:
    """Main ordering for cleaning lambda functions.

    Returns:
        A list of all terminated functions
    """
    print("Cleaning Lambda Functions")
    lambda_client = boto3.client("lambda")
    functions = get_functions(lambda_client)
    terminated_functions = delete_functions(lambda_client, functions)
    print("Terminated {0} Lambda Function/s".format(len(terminated_functions)))
    return terminated_functions


def get_functions(lambda_client) -> list:
    """Gets all the lambda functions in an account.

    Args:
        lambda_client: A lambda boto3 client.

    Returns:
        A list of all lambda functions in the account.
    """
    function_list = []
    paginator = lambda_client.get_paginator("list_functions")
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
        lambda_client.delete_function(
            FunctionName=lambda_function["FunctionName"]
        )
        terminated_functions.append(lambda_function["FunctionName"])
    return terminated_functions