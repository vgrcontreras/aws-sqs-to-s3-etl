from utils.aws_client import s3_client
from loguru import logger


def create_s3_bucket(bucket_name: str = 'aws-sqs-to-s3-etl-bucket') -> str:
    """
    Creates an AWS S3 bucket with the specified name.
    
    Args:
        bucket_name (str, optional): Name of the S3 bucket to create.
                                    Defaults to 'aws-sqs-to-s3-etl-bucket'.
                                    Must be globally unique across all AWS accounts.
                                    
    Returns:
        str: The name of the created S3 bucket, which can be used for
             storing and retrieving objects.
             
    Note:
        S3 bucket names must be globally unique. If the bucket already exists
        or the name is taken, an error will be logged.
        Logs the bucket creation status and any errors that occur.
    """
    try:
        s3_client.create_bucket(
            Bucket=bucket_name
        )
        logger.info(f'Bucket {bucket_name} created successfully')

        return bucket_name
    except Exception as e:
        logger.error(f'Error creating bucket: {e}')


if __name__ == '__main__':
    bucket_name = create_s3_bucket()