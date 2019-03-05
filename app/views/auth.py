import json
from datetime import datetime

from flask import Blueprint, Response, request
from flask_negotiate import consumes, produces
from jsonschema import FormatChecker, ValidationError, validate
from werkzeug.exceptions import BadRequest, Unauthorized

from app import db
from app.models import User

auth = Blueprint('auth', __name__)

# JSON schema for user requests
with open('openapi.json') as json_file:
    openapi = json.load(json_file)
login_schema = openapi["components"]["schemas"]["LoginRequest"]


@auth.route("/login", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def login_user():
    """Authenticate User by email address and password."""
    login_request = request.json

    # Validate request against schema
    try:
        validate(login_request, login_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Check user is registered
    user = User.query.filter_by(email_address=login_request["email_address"].lower()).first()
    if user is None:
        raise Unauthorized()

    # Check user credentials
    if user.check_password(login_request["password"]):
        user.login_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

        return Response(response=repr(user), mimetype='application/json', status=200)
    else:
        raise Unauthorized()
