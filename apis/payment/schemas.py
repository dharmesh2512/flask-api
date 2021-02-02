from datetime import datetime

from luhn.luhn import aLuhn
from marshmallow import Schema, ValidationError, fields, validates
from marshmallow.validate import Length


class PaymentProcessSchema(Schema):
    """
    Schema to validate payment process data
    """

    credit_card_number = fields.Str(required=True)
    card_holder_name = fields.Str(required=True, validate=Length(max=50))
    expiration_date = fields.Date(required=True, format="%m/%Y")
    security_code = fields.Int(required=True)
    amount = fields.Float(required=True)

    @validates("credit_card_number")
    def validate_credit_card_number(self, value):
        """Validate card number"""

        if not aLuhn.doLuhn(value):
            raise ValidationError("Invalid credit card number.")

    @validates("expiration_date")
    def validate_expiration_date(self, value):
        """'value' is the datetime parsed from expiration_date by marshmallow"""

        now = datetime.now().date()
        if value < now:
            raise ValidationError("Expiration date should be future date.")

    @validates("security_code")
    def validate_security_code(self, value):
        """Validate security code and it should be 3 digit only"""

        if len(str(value)) != 3:
            raise ValidationError("Invalid security code.")

    @validates("amount")
    def validate_amount(self, value):
        """Validate amount and it should be more than 0"""

        if value < 0:
            raise ValidationError("Amount should be more than 0.")
