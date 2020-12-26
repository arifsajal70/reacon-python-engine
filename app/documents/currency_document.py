# Import Mongoengine Things
from mongoengine import Document, fields


class Currency(Document):
    name = fields.StringField()
    short_code = fields.StringField()
    symbol = fields.StringField()
    exchange_rate = fields.FloatField()
    default = fields.BooleanField(default=False)
    can_withdraw = fields.BooleanField(default=False)
    can_pay = fields.BooleanField(default=False)
    type = fields.StringField(choices=['fiat', 'crypto'])

    meta = {
        "collection": "currencies",
        "ordering": ["+name"]
    }

    @classmethod
    def get_by_short_code(cls, short_code):
        """
        Get Single Currency By Short Code
        :param short_code:
        :return:
        """
        return cls.objects(short_code=short_code)
