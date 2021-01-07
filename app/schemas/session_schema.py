# Import Database Things
from marshmallow_mongoengine import ModelSchema, fields

# Import Documents
from app.documents.session_document import SessionDocument

# Import Schemas
from app.schemas.client_schema import Client as ClientSchema
from app.schemas.admin_schema import Admin as AdminSchema


class Session(ModelSchema):
    user = fields.Function(lambda obj: (obj.client and ClientSchema(many=False).dump(obj.client).data) or
                                       (obj.admin and AdminSchema(many=False).dump(obj.admin).data) or None)

    class Meta:
        model = SessionDocument
        exclude = ['admin', 'client', 'password']
