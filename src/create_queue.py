from utils.aws_client import sqs_client
from loguru import logger


def create_queue(queue_name: str = 'aws-sqs-to-s3-etl-queue') -> str:
    try:
        response = sqs_client.create_queue(
            QueueName=queue_name
        )
        logger.info(
            f'Queue create successfully. QueueUrl: {response['QueueUrl']}'
        )

        return response['QueueUrl']
    except Exception as e:
        logger.error(f'Error creating queue: {e}')


if __name__ == '__main__':
    queue_url = create_queue()