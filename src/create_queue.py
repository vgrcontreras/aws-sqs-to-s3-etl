from utils.aws_client import sqs_client
from loguru import logger


def create_queue(queue_name: str = 'aws-sqs-to-s3-etl-queue') -> str:
    """
    Creates an AWS SQS queue with the specified name.
    
    Args:
        queue_name (str, optional): Name of the SQS queue to create.
                                   Defaults to 'aws-sqs-to-s3-etl-queue'.
                                   
    Returns:
        str: The URL of the created SQS queue, which can be used for
             sending and receiving messages.
             
    Note:
        If the queue already exists, this will return the existing queue's URL.
        Logs the queue creation status and any errors that occur.
    """
    try:
        response = sqs_client.create_queue(
            QueueName=queue_name
        )
        logger.info(
            f"Queue create successfully. QueueUrl: {response['QueueUrl']}"
        )

        return response['QueueUrl']
    except Exception as e:
        logger.error(f'Error creating queue: {e}')


if __name__ == '__main__':
    queue_url = create_queue()