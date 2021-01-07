# Import Database Things
from mongoengine import Document, signals, fields

# Import Utils
import datetime


class Admin(Document):
    first_name = fields.StringField()
    last_name = fields.StringField()

    email = fields.EmailField()
    username = fields.StringField()
    password = fields.StringField()

    active = fields.BooleanField()

    created_at = fields.DateTimeField(required=False)
    updated_at = fields.DateTimeField(required=False)

    meta = {
        "collection": "admins",
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


signals.pre_save.connect(Admin.set_timings, sender=Admin)
