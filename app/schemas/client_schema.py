# Import Models
from app.documents.client_document import Client as ClientDocument

# Import Database Things
from marshmallow_mongoengine import ModelSchema, fields


class Client(ModelSchema):
    full_name = fields.Function(lambda obj: (obj.first_name and obj.first_name + ' ' or '') +
                                            (obj.middle_name and obj.middle_name + ' ' or '') +
                                            (obj.last_name and obj.last_name or ''))
    total_balance = fields.Function(
        lambda obj: float((obj.balance.bonus or 0) + (obj.balance.referral or 0) + (obj.balance.referral or 0)))

    class Meta:
        model = ClientDocument
        exclude = ['password']
