import boto3
from utils.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, REGION_NAME


sqs_client = boto3.client(
    'sqs',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

