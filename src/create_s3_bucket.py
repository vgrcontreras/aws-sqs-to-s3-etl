from utils.aws_client import s3_client
from loguru import logger


def create_s3_bucket(bucket_name: str = 'aws-sqs-to-s3-etl-bucket') -> str:
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