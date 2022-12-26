import datetime
import random
import string

import httpx

from core.config import config


def generate_code(len_promo: int = None) -> str | None:
    """
    This function generate unique promo code from user.
    :param len_promo: number of characters in the promo code.
    :return: unique format string.
    """
    len_promo = len_promo or random.randint(5, 10)
    return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=len_promo))


async def send_email(users_ids: list[int], code: str, discount_percents: int) -> None:
    now = datetime.datetime.now().isoformat()
    async with httpx.AsyncClient() as client:
        for user_id in users_ids:
            await client.post(
                url=f"{config.notifier_api_url}/notifier/v1/notifications/notification",
                json={
                    "users_ids": [user_id],
                    "template_name": "promo.html",
                    "status": "created",
                    "channel": "email",
                    "category": "promo",
                    "variables": {
                        "promo_code": code,
                        "discount_percents": discount_percents,
                        "text": "А вот вам промокод",
                        "subject": "Персональный промокод",
                    },
                    "send_time": now,
                },
            )
