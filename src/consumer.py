from utils.aws_client import sqs_client, s3_client
from loguru import logger
from datetime import datetime
from pathlib import Path
import os
import json
from typing import Dict, Any


def receive_sqs_message(queue_url: str) -> Dict[str, Any]:
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


def convert_msg_to_json_files(messages: list[dict]) -> None:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    folder_path = 'data'
    file_name = f'users_{timestamp}.json'

    os.makedirs(folder_path, exist_ok=True)
    
    with open(f'{folder_path}/{file_name}', 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)
        logger.info(f'File {file_name} created successfully')

    return os.path.join(folder_path, file_name)


def delete_sqs_message(queue_url: str, receipt_handle: str) -> None:
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle 
        )
        logger.info(f'Deleted message {receipt_handle} successfully')
    except Exception as e:
        logger.error(f'Error deleting message: {e}')


def upload_file_to_s3(file_name: str, bucket_name: str, key: str) -> None:
    try:
        s3_client.upload_file(file_name, bucket_name, key)
        logger.info(f'{file_name} uploaded to {bucket_name} successfully')
    except Exception as e:
        logger.error(f'Error loading {file_name} to {bucket_name}: {e}')


def consumer_main(queue_url: str, bucket_name: str) -> None:
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
