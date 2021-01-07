# Import flask Things
from flask import request

# Import Documents
from app.documents.session_document import SessionDocument
from app.documents.client_document import Client as ClientDocument
from app.documents.admin_document import Admin as AdminDocument

# Import Schemas
from app.schemas.session_schema import Session as SessionSchema

# Import Utils
import hashlib
import datetime


def set_current_session(user=None):
    """
    Set Session For Specific User
    :param user:
    :return:
    """
    if user is not None:
        current_time = datetime.datetime.utcnow()
        token = hashlib.sha256(request.user_agent.__str__().encode('utf-8') + current_time.__str__().encode('utf-8') + user['id'].__str__().encode('utf-8'))

        if isinstance(user, ClientDocument) or isinstance(user, AdminDocument):
            session = get_previous_active_session(user)
            if session is False:
                session = SessionDocument(
                    user_agent=request.user_agent.__str__(),
                    client=isinstance(user, ClientDocument) and user or None,
                    admin=isinstance(user, AdminDocument) and user or None,
                    type=(isinstance(user, ClientDocument) and 'client') or (isinstance(user, AdminDocument) and 'admin'),
                    token=token.hexdigest(),
                    expiration=current_time + datetime.timedelta(hours=6),
                    date_created=current_time
                ).save()

            return session
    return False


def get_current_session(formatted=True):
    """
    Get Current Session By Header Auth Token
    :param formatted:
    :return:
    """
    token = request.headers.get('auth-key')
    session = SessionDocument.objects(
        user_agent=request.user_agent.__str__(),
        token=token,
    ).first()

    session_expired = check_if_expire_session(session)

    if session and not session_expired:
        if formatted:
            return SessionSchema.dump(session).data
        else:
            return session

    return None


def get_current_user():
    """
    Get Current User
    :return:
    """
    current_session = get_current_session(formatted=False)
    return current_session.admin or current_session.client


def get_previous_active_session(user):
    if user:
        session = SessionDocument.objects(
            client=isinstance(user, ClientDocument) and user or None,
            admin=isinstance(user, AdminDocument) and user or None,
            user_agent=request.user_agent.__str__(),
            expiration__gte=datetime.datetime.utcnow(),
            type=(isinstance(user, ClientDocument) and 'client') or (isinstance(user, AdminDocument) and 'admin')
        ).first()
        return session and session or False
    return False


def update_token_expiration():
    """
    Update Token Expiration
    :return:
    """
    session = get_current_session(formatted=False)
    if session:
        session.update(
            expiration=datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        )


def remove_current_session():
    """
    Remove Current Session
    :return:
    """
    current_session = get_current_session(formatted=False)

    if current_session.delete():
        return True
    return False


def check_if_expire_session(session):
    """
    Delete Expire Session
    :param session:
    :return:
    """
    if session is not None and session['expiration'] < datetime.datetime.utcnow():
        return True
    return False


def check_session_if_admin():
    """
    Check If Session Is For Admin
    :return:
    """
    session = get_current_session(False)
    if session.type == 'admin':
        return True
    return False


def check_session_if_user():
    """
    Check If Session Is For User
    :return:
    """
    session = get_current_session(False)
    if session.type == 'user':
        return True
    return False
