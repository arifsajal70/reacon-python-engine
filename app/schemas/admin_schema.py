# Import Models
from app.documents.admin_document import Admin as AdminDocument

# Import Database Things
from marshmallow_mongoengine import ModelSchema, fields


class Admin(ModelSchema):
    full_name = fields.Function(lambda obj: (obj.first_name and obj.first_name + ' ' or '') +
                                            (obj.last_name and obj.last_name or ''))

    class Meta:
        model = AdminDocument
        exclude = ['password']
