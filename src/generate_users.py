from faker import Faker
import json

fake = Faker()

def create_user() -> str:
    """
    Creates a fake user with random data using the Faker library.
    
    Returns:
        str: JSON string containing user data with the following fields:
             - first_name: Random first name
             - last_name: Random last name  
             - email: Random email address
             - created_at: Random date
             
    Example:
        >>> user_json = create_user()
        >>> # Returns something like:
        >>> # '{"first_name": "John", "last_name": "Doe", 
        >>> #   "email": "john.doe@example.com", "created_at": "2023-01-15"}'
    """
    user = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'created_at': fake.date()
    }

    return json.dumps(user)

