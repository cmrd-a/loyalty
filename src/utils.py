import random
import string


def generate_code(len_promo: int = None) -> str:
    """
    This function generate unique promo code from user.
    :param len_promo: number of characters in the promo code.
    :return: unique format string.
    """
    len_promo = len_promo or random.randint(5, 10)
    return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=len_promo))
