import uuid as uuidlib


def generate_random_uuid():
    # Generate a UUID as a confirmation key
    return str(uuidlib.uuid4())
