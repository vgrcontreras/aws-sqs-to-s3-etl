from faker import Faker
import json

fake = Faker()

def create_user() -> str:
    user = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'created_at': fake.date()
    }

    return json.dumps(user)

