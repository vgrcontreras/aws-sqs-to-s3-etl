from src.generate_users import create_user
from src.create_queue import create_queue
from src.producer import sqs_send_message
from src.create_s3_bucket import create_s3_bucket
from src.consumer import consumer_main
import random

def main() -> None:
    """
    Main orchestration function for the AWS SQS to S3 ETL pipeline.
    
    This function coordinates the entire ETL (Extract, Transform, Load) process:
    1. Creates an SQS queue for message handling
    2. Generates random user data and sends it to the queue
    3. Creates an S3 bucket for data storage
    4. Processes all messages from the queue and uploads them to S3
    
    The number of users generated is random between 1 and 10.
    """
    queue_url = create_queue()

    for _ in range(0, random.randint(1, 10)):
        user = create_user()
        sqs_send_message(queue_url=queue_url, message=user)

    bucket_name = create_s3_bucket()
    consumer_main(queue_url=queue_url, bucket_name=bucket_name)


if __name__ == '__main__':
    main()