from src.generate_users import create_user
from src.create_queue import create_queue
from src.producer import sqs_send_message
from src.create_s3_bucket import create_s3_bucket
from src.consumer import consumer_main
import random

def main() -> None:
    queue_url = create_queue()

    for _ in range(0, random.randint(1, 10)):
        user = create_user()
        sqs_send_message(queue_url=queue_url, message=user)

    bucket_name = create_s3_bucket()
    consumer_main(queue_url=queue_url, bucket_name=bucket_name)


if __name__ == '__main__':
    main()