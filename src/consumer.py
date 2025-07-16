from utils.aws_client import sqs_client, s3_client
from loguru import logger
from datetime import datetime
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
        logger.info('SQS Message received successfully')

        return response
    except Exception as e:
        logger.error(f'Error receiving SQS messages: {e}')
        return {}


def convert_msg_to_json_files(messages: list[dict]) -> None:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    file_path = 'data'
    file_name = f'users_{timestamp}.json'

    os.makedirs(file_path, exist_ok=True)
    
    with open(f'{file_path}/{file_name}', 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)
        logger.info(f'File {file_name} created successfully')


def delete_sqs_message(queue_url: str, receipt_handle: str) -> None:
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        logger.info(f'Deleted message {receipt_handle} successfully')
    except Exception as e:
        logger.error(f'Error deleting message: {e}')


def upload_file_to_s3():
    pass


def consumer_main(queue_url: str) -> None:
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

    convert_msg_to_json_files(bodies)
    

if __name__ == '__main__':
    consumer_main('https://sqs.us-east-1.amazonaws.com/203918857534/test')