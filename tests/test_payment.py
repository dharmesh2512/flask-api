import json
import random
import unittest

import faker as faker
from faker import Faker

from main import app


class PaymentTest(unittest.TestCase):
    def setUp(self):
        self.api_client = app.test_client
        self.fake = Faker()

    def request(self, payload):
        return self.api_client().post(
            "/api/process/payment",
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_payment_process_invalid_data(self):
        """
        Testcase to validate payment data
        """
        response = self.request(
            {
                "credit_card_number": self.fake.credit_card_number(),
                "card_holder_name": self.fake.name(),
                "expiration_date": self.fake.credit_card_expire(),
                "security_code": random.randint(1000, 5000),
                "amount": 10,
            }
        )

        self.assertEqual(400, response.status_code)

    def test_payment_process_cheap_gateway(self):
        """
        Testcase to make payment with cheap payment gateway
        """
        response = self.request(
            {
                "credit_card_number": self.fake.credit_card_number(),
                "card_holder_name": self.fake.name(),
                "expiration_date": "11/2021",
                "security_code": random.randint(100, 999),
                "amount": random.randint(1, 10),
            }
        )

        self.assertEqual(200, response.status_code)
        payment_id = response.json["data"]["payment_id"]
        self.assertTrue(payment_id.startswith("cheap"))

    def test_payment_process_expensive_gateway(self):
        """
        Testcase to make payment with expensive payment gateway
        """
        response = self.request(
            {
                "credit_card_number": self.fake.credit_card_number(),
                "card_holder_name": self.fake.name(),
                "expiration_date": "11/2021",
                "security_code": random.randint(100, 999),
                "amount": random.randint(20, 500),
            }
        )

        self.assertEqual(200, response.status_code)
        payment_id = response.json["data"]["payment_id"]
        self.assertTrue(payment_id.startswith("expensive"))

    def test_payment_process_premium_gateway(self):
        """
        Testcase to make payment with premium payment gateway
        """
        response = self.request(
            {
                "credit_card_number": self.fake.credit_card_number(),
                "card_holder_name": self.fake.name(),
                "expiration_date": "11/2021",
                "security_code": self.fake.credit_card_security_code(),
                "amount": random.randrange(500, 1000),
            }
        )

        self.assertEqual(200, response.status_code)
        payment_id = response.json["data"]["payment_id"]
        self.assertTrue(payment_id.startswith("premium"))
