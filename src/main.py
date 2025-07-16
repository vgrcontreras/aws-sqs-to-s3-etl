from src.generate_users import create_user
from src.create_queue import create_queue
from src.producer import sqs_send_message
from src.create_s3_bucket import create_s3_bucket
import random

def main() -> None:
    queue_url = create_queue(queue_name='test')  # remover queue name para default

    for _ in range(0, random.randint(1, 5)):
        user = create_user()
        sqs_send_message(queue_url=queue_url, message=user)

    bucket_name = create_s3_bucket()


if __name__ == '__main__':
    main()