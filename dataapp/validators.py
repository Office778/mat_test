import re

def is_valid_password(password):
    """
    Validates that the password:
    - is at least 8 characters long
    - has at least one uppercase letter
    - has at least one lowercase letter
    - has at least one digit
    - has at least one special character
    """
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[\W_]', password)
    )
