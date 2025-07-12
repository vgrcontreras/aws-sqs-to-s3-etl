from faker import Faker

fake = Faker()

def create_user() -> dict:
    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'created_at': fake.date()
    }


