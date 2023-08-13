import random
import string


def businessIDGenerator():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=12
        )
    )


def apiKeyGenerator():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=64
        )
    )


