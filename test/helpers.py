import random
import string


def get_n_random(n: int) -> list:
    return [random.random() for _ in range(n)]


def get_random_text(n: int) -> str:
    return ''.join(random.choices(population=string.ascii_letters, k=n))

