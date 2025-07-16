from utils.aws_client import sqs_client, s3_client
from loguru import logger
from datetime import datetime
import os
import json
from typing import Dict, Any


def receive_sqs_message(queue_url: str) -> Dict[str, Any]:
    """
    Receives messages from an AWS SQS queue.
    
    Args:
        queue_url (str): The URL of the SQS queue to receive messages from.
        
    Returns:
        Dict[str, Any]: The response from SQS containing messages and metadata.
                       Returns empty dict if an error occurs.
                       
    Note:
        Configures long polling with 10 second wait time and retrieves up to 10 messages.
    """
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )
        logger.info(f'Request queue message in {queue_url} done sucessfully')

        return response
    except Exception as e:
        logger.error(f'Error receiving SQS messages: {e}')
        return {}


def convert_msg_to_json_files(messages: list[dict]) -> str:
    """
    Converts a list of messages to a JSON file with timestamp-based naming.
    
    Args:
        messages (list[dict]): List of message dictionaries to be saved as JSON.
        
    Returns:
        str: The file path of the created JSON file.
        
    Note:
        Creates a 'data' directory if it doesn't exist. The file is named with
        a timestamp pattern: users_YYYYMMDD_HHMMSS.json
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    folder_path = 'data'
    file_name = f'users_{timestamp}.json'

    os.makedirs(folder_path, exist_ok=True)
    
    with open(f'{folder_path}/{file_name}', 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)
        logger.info(f'File {file_name} created successfully')

    return os.path.join(folder_path, file_name)


def delete_sqs_message(queue_url: str, receipt_handle: str) -> None:
    """
    Deletes a specific message from an AWS SQS queue.
    
    Args:
        queue_url (str): The URL of the SQS queue containing the message.
        receipt_handle (str): The receipt handle of the message to delete.
                             This is obtained when receiving the message.
                             
    Note:
        Logs success or failure of the deletion operation.
    """
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle 
        )
        logger.info(f'Deleted message {receipt_handle} successfully')
    except Exception as e:
        logger.error(f'Error deleting message: {e}')


def upload_file_to_s3(file_name: str, bucket_name: str, key: str) -> None:
    """
    Uploads a local file to an AWS S3 bucket.
    
    Args:
        file_name (str): Path to the local file to upload.
        bucket_name (str): Name of the S3 bucket destination.
        key (str): The S3 object key (path/filename) for the uploaded file.
        
    Note:
        Logs success or failure of the upload operation.
    """
    try:
        s3_client.upload_file(file_name, bucket_name, key)
        logger.info(f'{file_name} uploaded to {bucket_name} successfully')
    except Exception as e:
        logger.error(f'Error loading {file_name} to {bucket_name}: {e}')


def consumer_main(queue_url: str, bucket_name: str) -> None:
    """
    Main consumer function that processes all messages from SQS and uploads them to S3.
    
    This function:
    1. Continuously polls the SQS queue for messages
    2. Collects all message bodies
    3. Deletes processed messages from the queue
    4. Converts collected messages to a JSON file
    5. Uploads the file to S3
    6. Cleans up the local file
    
    Args:
        queue_url (str): The URL of the SQS queue to consume from.
        bucket_name (str): The name of the S3 bucket to upload to.
        
    Note:
        Stops processing when no more messages are available in the queue.
        Automatically cleans up the local JSON file after successful S3 upload.
    """
    bodies = []

    while True:
        response = receive_sqs_message(queue_url=queue_url)

        if 'Messages' in response:
            for message in response.get('Messages'):
                msg_body = message['Body']
                bodies.append(msg_body)

                delete_sqs_message(
                    queue_url=queue_url,
                    receipt_handle=message['ReceiptHandle']
                )

        else:
            logger.info('No messages in queue')
            break
    
    try:
        file_path = convert_msg_to_json_files(bodies)
        upload_file_to_s3(file_path, bucket_name, os.path.basename(file_path))
        os.remove(file_path)
    except Exception as e:
        logger.error(e)
