# Import Schemas
from app.schemas.session_schema import Session as SessionSchema

# Import Helpers
from app.helpers.response import Response
from app.helpers.session import set_current_session, get_current_session
from app.helpers.auth import check_authentication

# Import Validators
from app.validator import login_validator

# Import Utils
import time


@login_validator
def login():
    user = check_authentication()
    time.sleep(5)

    if user is not False:
        session = set_current_session(user)
        if session:
            sess = SessionSchema(many=False).dump(session).data
            return Response(data=sess, message='Signed In Successfully').send()
        else:
            return Response(message='Can\'t Sign In Now, Please Contact Administrator.', status_code=403).send()

    else:
        return Response(message='Invalid Credentials, Please Try With Another One.', status_code=403).send()


def logout():
    session = get_current_session(formatted=False)
    if session:
        session.delete()

    return Response(message='Logged Out Successfully.').send()
