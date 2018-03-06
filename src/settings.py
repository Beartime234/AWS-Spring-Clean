# settings.py

# aws-clean will not destroy things in the whitelist for global resources
# please put under the global region. I recommend just adding to the lists provided


# What value do i put in for each resource

# s3_buckets - BucketName
# ec2_instances - Instance-id
# rds_instances - DbIndentifier
# dynamo_tables - TableName
# redshift_clusters - ClusterIdentifier
# ecs_clusters - Cluster ARN
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

        ],
        "redshift_clusters": [

        ],
        "ecs_clusters": [

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

        ],
        "redshift_clusters": [

        ],
        "ecs_clusters": [

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
