import random
import string


def rand_id(id_length):
    rand_chars = random.sample(string.digits + string.ascii_letters, id_length)
    return "".join(rand_chars)


def rand_id_list(size, id_length):
    """Generate a list of guaranteed unique ids"""

    rand_ids = set()

    while len(rand_ids) < size:
        rand_ids.add(rand_id(id_length))

    return sorted(rand_ids)
