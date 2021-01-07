# Import Database Things
from mongoengine import Document, StringField, DateTimeField, ReferenceField

# Import Documents
from app.documents.client_document import Client as ClientDocument
from app.documents.admin_document import Admin as AdminDocument


class SessionDocument(Document):
    user_agent = StringField(required=True, max_length=512)
    client = ReferenceField(required=False, document_type=ClientDocument)
    admin = ReferenceField(required=False, document_type=AdminDocument)
    type = StringField(choices=['admin', 'client'])
    expiration = DateTimeField(required=True)
    token = StringField(max_length=256, required=True)
    date_created = DateTimeField(required=True)

    meta = {
        "collection": "sessions",
        "ordering": ["-date_created"]
    }
