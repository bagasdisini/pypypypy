import random
import string
import bcrypt


def random_string(length: int) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
