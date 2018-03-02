# settings.py

# Changeable Settings
WHITELIST = {
    "global": {
        "s3_buckets": [

        ]
    },
    "us-east-1": {
        "ec2_instances": [],
        "rds_instances": [],
        "lambda_functions": []
    },
    "us-east-2": {
        "ec2_instances": [],
        "rds_instances": [],
        "lambda_functions": []
    }
}
REGIONS = [
    "us-east-1",
    "us-east-2"
]
RESULTS_DIR = "results"
RESULTS_FILENAME = "aws-clean"
