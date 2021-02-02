import hashlib
from uuid import uuid4

from utils.constants import STATUS


class PremiumPaymentGateway(object):
    @staticmethod
    def charge(
        credit_card_number,
        card_holder_name,
        expiration_date,
        security_code,
        amount,
        attempt=1,
    ):
        if attempt != 4:
            return {
                "status": STATUS.get("ERROR"),
                "message": "Invalid credential to perform this action.",
            }

        hash_object = hashlib.md5(
            (str(credit_card_number) + card_holder_name + str(security_code)).encode()
        )

        return {
            "status": STATUS.get("SUCCESS"),
            "data": {
                "payment_id": "premium_" + str(uuid4()),
                "payment_token": hash_object.hexdigest(),
            },
        }
