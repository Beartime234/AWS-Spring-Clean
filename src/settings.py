# settings.py

# aws-clean will not destroy things in the whitelist for global resources
# please put under the global region. I recommend just adding to the lists
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
# regions that aws-clean will go through. Global is things like S3 and IAM
REGIONS = [
    "global",
    "us-east-1",
    "us-east-2"
]
RESULTS_DIR = "results"
RESULTS_FILENAME = "aws-clean"