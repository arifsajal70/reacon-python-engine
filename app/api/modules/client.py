# Import Documents
from app.documents.client_document import Client as ClientDocument

# Import Schemas
from app.schemas.client_schema import Client as ClientSchema

# Import Helpers
from app.helpers.table import DataTable
from app.helpers.response import Response

# Import Utils
import bson


def get_clients():
    """
    Get Client List With Pagination
    :return:
    """
    data = DataTable(document=ClientDocument, schema=ClientSchema).get_data
    return Response(data=data).send()


def get_client(client_id):
    """
    Get Single Client
    :param client_id:
    :return:
    """
    if bson.objectid.ObjectId.is_valid(client_id):
        client = ClientDocument.objects(id=client_id).first()
        if client:
            return Response(data=ClientSchema(many=False).dump(client).data).send()
        return Response(message='No Client Found With The Given ID', status_code=404).send()
    return Response(message='Invalid Client Id Given.', status_code=403).send()
