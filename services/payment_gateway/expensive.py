import hashlib

from uuid import uuid4

from utils.constants import STATUS


class ExpensivePaymentGateway(object):
    @staticmethod
    def charge(
        credit_card_number, card_holder_name, expiration_date, security_code, amount
    ):
        hash_object = hashlib.md5(
            (str(credit_card_number) + card_holder_name + str(security_code)).encode()
        )
        return {
            "status": STATUS.get("SUCCESS"),
            "data": {
                "payment_id": "expensive_" + str(uuid4()),
                "payment_token": hash_object.hexdigest(),
            },
        }
