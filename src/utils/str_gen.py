import random
import string


def get_username(length: int = 7) -> str:
    pool = string.ascii_letters
    return "".join(random.choice(pool) for _ in range(length))
