# Import Mongoengine Things
from mongoengine import Document, fields, signals, EmbeddedDocument

# Import Documents
from app.documents.country_document import Country as CountryDocument
from app.documents.currency_document import Currency as CurrencyDocument

# Import Utilities
import datetime


class Referrals(EmbeddedDocument):
    level = fields.IntField()
    Client = fields.ReferenceField(document_type='Client')
    bonus = fields.DecimalField(rounding=3)

    meta = {
        'ordering': ['+level']
    }


class Balance(EmbeddedDocument):
    purchased = fields.IntField(default=0)
    bonus = fields.IntField(default=0)
    referral = fields.IntField(default=0)


class Wallets(EmbeddedDocument):
    currency = fields.ReferenceField(CurrencyDocument)
    address = fields.StringField()
    created_at = fields.DateTimeField()

    meta = {
        'ordering': ['-created_at']
    }


class EmailVerification(EmbeddedDocument):
    is_verified = fields.BooleanField(default=False)
    verified_at = fields.DateTimeField(required=False, default=None)


class Client(Document):
    first_name = fields.StringField()
    middle_name = fields.StringField(required=False)
    last_name = fields.StringField(required=False)
    mobile = fields.StringField(required=False),
    date_of_birth = fields.DateTimeField(required=False),
    nationality = fields.ReferenceField(document_type=CountryDocument, required=False)

    email = fields.EmailField(unique=True, required=True)
    email_verification = fields.EmbeddedDocumentField(document_type=EmailVerification, default=EmailVerification())
    username = fields.StringField(unique=True, required=True)
    password = fields.StringField(required=True)
    active = fields.BooleanField(default=False)

    referrals = fields.EmbeddedDocumentListField(document_type=Referrals)
    balance = fields.EmbeddedDocumentField(document_type=Balance, default=Balance())
    wallets = fields.EmbeddedDocumentListField(document_type=Wallets)

    created_at = fields.DateTimeField(required=False)
    updated_at = fields.DateTimeField(required=False)

    meta = {
        "collection": "clients",
        "ordering": ["-created_at"]
    }

    @classmethod
    def set_timings(cls, sender, document, **kwargs):
        """
        Set Created At On Save
        :return:
        """
        if 'created_at' not in kwargs and not document.created_at:
            document.created_at = datetime.datetime.utcnow()

        document.updated_at = datetime.datetime.utcnow()

    @classmethod
    def get_by_activation(cls, active=True):
        """
        Return Query With Active Status
        :param active:
        :return:
        """
        return cls.objects(active=active)

    @classmethod
    def get_by_username(cls, username):
        """
        Return Single User By Username
        :param username:
        :return:
        """
        return cls.objects(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        """
        Return Single User By Email
        :param email:
        :return:
        """
        return cls.objects(email=email).first()

    def increase_balance(self, amount, to):
        """
        Increase Balance
        :param amount:
        :param to:
        :return:
        """
        if to in ['purchased', 'bonus', 'referral']:
            if to == 'purchased':
                self.update(
                    balance__purchased=self.balance.purchased + amount
                )
            elif to == 'bonus':
                self.update(
                    balance__bonus=self.balance.bonus + amount
                )
            elif to == 'referral':
                self.update(
                    balance__referral=self.balance.referral + amount
                )

    def decrease_balance(self, amount, to):
        """
        Decrease Balance
        :param amount:
        :param to:
        :return:
        """
        if to in ['purchased', 'bonus', 'referral']:
            if to == 'purchased':
                self.update(
                    balance__purchased=self.balance.purchased - amount
                )
            elif to == 'bonus':
                self.update(
                    balance__bonus=self.balance.bonus - amount
                )
            elif to == 'referral':
                self.update(
                    balance__referral=self.balance.referral - amount
                )


signals.pre_save.connect(Client.set_timings, sender=Client)
