import json
from datetime import datetime

from flask import Blueprint, Response, request, url_for
from flask_negotiate import consumes, produces
from jsonschema import FormatChecker, ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from app import db
from app.models import User

user = Blueprint('user', __name__)

# JSON schema for user requests
with open('openapi.json') as json_file:
    openapi = json.load(json_file)
user_schema = openapi["components"]["schemas"]["UserRequest"]
profile_schema = openapi["components"]["schemas"]["ProfileRequest"]
password_schema = openapi["components"]["schemas"]["PasswordRequest"]
login_schema = openapi["components"]["schemas"]["LoginRequest"]


@user.route("", methods=['GET'])
@produces('application/json')
def get_users():
    """Get Users."""
    email_query = request.args.get('email_address', type=str)

    if email_query is not None:
        user = User.query.filter_by(email_address=email_query).first_or_404()
        result = user.as_dict()
    else:
        raise BadRequest("'email_address' is a required query parameter")

    return Response(response=json.dumps(result, sort_keys=True, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@user.route("", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_user():
    """Create a new User."""
    user_request = request.json

    # Validate request against schema
    try:
        validate(user_request, user_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Create a new user object
    user = User(
        password=user_request["password"],
        first_name=user_request["first_name"],
        last_name=user_request["last_name"],
        email_address=user_request["email_address"]
    )

    try:
        # Commit user to db
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise Conflict("'email_address' is already registered.")

    # Create response
    response = Response(response=repr(user), mimetype='application/json', status=201)
    response.headers["Location"] = url_for('user.get_user', id=user.id)

    return response


@user.route("/<uuid:id>", methods=['GET'])
@produces('application/json')
def get_user(id):
    """Get a User for a given id."""
    user = User.query.get_or_404(str(id))

    return Response(response=repr(user),
                    mimetype='application/json',
                    status=200)


@user.route("/<uuid:id>/profile", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_user_profile(id):
    """Update a User profile for a given id."""
    profile_request = request.json

    # Validate request against schema
    try:
        validate(profile_request, profile_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Retrieve existing user
    user = User.query.get_or_404(str(id))

    # Update user
    user.first_name = profile_request["first_name"].title(),
    user.last_name = profile_request["last_name"].title(),
    user.email_address = profile_request["email_address"].lower()
    user.updated_at = datetime.utcnow()

    try:
        # Commit user to db
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise Conflict("'email_address' is already registered.")

    return Response(response=repr(user),
                    mimetype='application/json',
                    status=200)


@user.route("/<uuid:id>/password", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_user_password(id):
    """Update a User password for a given id."""
    password_request = request.json

    # Validate request against schema
    try:
        validate(password_request, password_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    if password_request["new_password"] == password_request["current_password"]:
        raise BadRequest("New password must be different to current password")

    # Retrieve existing user
    user = User.query.get_or_404(str(id))

    # Update user
    if user.check_password(password_request["current_password"]):
        user.set_password(password_request["new_password"])
        user.updated_at = datetime.utcnow()

        # Commit user to db
        db.session.add(user)
        db.session.commit()

        return Response(response=repr(user),
                        mimetype='application/json',
                        status=200)
    else:
        raise Unauthorized()


@user.route("/<uuid:id>", methods=['DELETE'])
@produces('application/json')
def delete_user(id):
    """Delete a User for a given id."""
    user = User.query.get_or_404(str(id))

    # If user has children that will have no users as a result of deleting this user, delete those children too.
    # This also results in events for that child being deleted too, by way of the foreign key cascade.
    if len(user.children) > 0:
        for child in user.children:
            if len(child.users) == 1:
                db.session.delete(child)

    db.session.delete(user)
    db.session.commit()
    return Response(response=None,
                    mimetype='application/json',
                    status=204)
