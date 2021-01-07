# Import Documents
from app.documents.admin_document import Admin as AdminDocument
from app.documents.client_document import Client as ClientDocument

# Import Flask Things
from flask import request

# Import Utils
import bcrypt


def check_authentication():
    data = request.values

    admin_by_username = AdminDocument.get_by_username(data.get('username'))
    if admin_by_username is not None:
        return check_password(admin_by_username)

    admin_by_email = AdminDocument.get_by_email(data.get('username'))
    if admin_by_email is not None:
        return check_password(admin_by_email)

    client_by_username = ClientDocument.get_by_username(data.get('username'))
    if client_by_username is not None:
        return check_password(client_by_username)

    client_by_email = ClientDocument.get_by_email(data.get('username'))
    if client_by_email is not None:
        return check_password(client_by_email)

    return False


def check_password(user):
    data = request.values

    return bcrypt.checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')) and user or False
