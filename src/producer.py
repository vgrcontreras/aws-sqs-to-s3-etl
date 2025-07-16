from utils.aws_client import sqs_client
from src.create_queue import create_queue
from loguru import logger

def sqs_send_message(queue_url: str, message: str) -> None:
    """
    Sends a message to an AWS SQS queue.
    
    Args:
        queue_url (str): The URL of the SQS queue to send the message to.
        message (str): The message body to send. Should be a string representation
                      of the data (e.g., JSON string).
                      
    Note:
        Logs success or failure of the message sending operation.
    """
    try:
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
        logger.info('Message send to queue successfully.')
    except Exception as e:
        logger.error(f'Erro sending message: {e}')


if __name__ == '__main__':
    queue_url = create_queue()
    sqs_send_message(queue_url=queue_url, message='test')