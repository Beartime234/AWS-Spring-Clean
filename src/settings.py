# settings.py

# aws-clean will not destroy things in the whitelist for global resources
# please put under the global region. I recommend just adding to the lists provided
WHITELIST = {
    "global": {
        "s3_buckets": [

        ]
    },
    "us-east-1": {
        "ec2_instances": [

        ],
        "rds_instances": [

        ],
        "lambda_functions": [

        ],
        "dynamo_tables": [

        ]
    },
    "us-east-2": {
        "ec2_instances": [

        ],
        "rds_instances": [

        ],
        "lambda_functions": [

        ],
        "dynamo_tables": [

        ]
    }
}
# regions that aws-clean will go through. global is things like S3 and IAM
REGIONS = [
    "global",
    "us-east-1",
    "us-east-2"
]
RESULTS_DIR = "results"
RESULTS_FILENAME = "aws_clean"
