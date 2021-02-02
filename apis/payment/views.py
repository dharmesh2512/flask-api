from http import HTTPStatus

from flask_restful import Resource

from flask import request

from apis.payment.schemas import PaymentProcessSchema
from services.payment_gateway.cheap import CheapPaymentGateway
from services.payment_gateway.expensive import ExpensivePaymentGateway
from services.payment_gateway.premium import PremiumPaymentGateway
from utils.constants import STATUS
from utils.exception_handler import ValidationError
from utils.response_handler import success_response, error_response


class ProcessPaymentAPI(Resource):
    """
    API to process payment using payment gateway (Cheap, Expensive, Premium).
    """

    def post(self):
        try:
            payment_process_schema = PaymentProcessSchema()

            json_data = request.get_json(force=True)
            errors = payment_process_schema.validate(json_data)

            if errors:
                raise ValidationError(
                    "Invalid parameters of process payment", error_message=errors
                )

            data = payment_process_schema.load(json_data)

            # payment process with gateway
            response = self.execute_payment(**data)

            if response.get("Status") == STATUS.get("ERROR"):
                return error_response(
                    code=HTTPStatus.BAD_GATEWAY,
                    status=STATUS.get("ERROR"),
                    error_message="Failed to perform payment process",
                )

            return success_response(
                status=STATUS.get("SUCCESS"),
                code=HTTPStatus.OK,
                message="Payment executed successfully",
                data=response.get("data"),
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            return error_response(
                code=HTTPStatus.INTERNAL_SERVER_ERROR,
                status="Error",
                error_message="Something went wrong, please try again",
            )

    def execute_payment(
        self,
        credit_card_number,
        card_holder_name,
        expiration_date,
        security_code,
        amount,
    ):
        """
        Execute payment with different payment gateway based on amount

        """
        if amount <= 20:
            response = CheapPaymentGateway.charge(
                credit_card_number,
                card_holder_name,
                expiration_date,
                security_code,
                amount,
            )
        elif 20 < amount <= 500:
            response = ExpensivePaymentGateway.charge(
                credit_card_number,
                card_holder_name,
                expiration_date,
                security_code,
                amount,
            )
        else:
            attempt = 1
            while True:
                response = PremiumPaymentGateway.charge(
                    credit_card_number,
                    card_holder_name,
                    expiration_date,
                    security_code,
                    amount,
                    attempt=attempt,
                )

                if response.get("status") == STATUS.get("SUCCESS"):
                    break

                if response.get("status") == STATUS.get("ERROR"):
                    attempt += 1

                if attempt > 4 and response.get("status") == STATUS.get("ERROR"):
                    break

        return response
