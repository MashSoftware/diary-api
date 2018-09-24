import json
from datetime import datetime

from flask import Blueprint, Response, request
from flask_negotiate import consumes, produces
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from app import db
from app.models import Child, User
from jsonschema import FormatChecker, ValidationError, validate

user = Blueprint('user', __name__)

# JSON schema for user requests
with open('openapi.json') as json_file:
    openapi = json.load(json_file)
user_schema = openapi["components"]["schemas"]["UserRequest"]
login_schema = openapi["components"]["schemas"]["LoginRequest"]


@user.route("/users", methods=['GET'])
@produces('application/json')
def get_users():
    """Get Users."""
    email_query = request.args.get('email_address', type=str)

    if email_query is not None:
        user = User.query.filter_by(email_address=email_query).first_or_404()
        result = user.as_dict()
    else:
        users = User.query.order_by(User.created_at).all()
        result = []
        for user in users:
            result.append(user.as_dict())

    return Response(response=json.dumps(result, sort_keys=True, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@user.route("/users", methods=['POST'])
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
    response.headers["Location"] = "{0}/{1}".format(request.url, user.id)

    return response


@user.route("/users/<uuid:id>", methods=['GET'])
@produces('application/json')
def get_user(id):
    """Get a User for a given id."""
    user = User.query.get_or_404(str(id))

    return Response(response=repr(user),
                    mimetype='application/json',
                    status=200)


@user.route("/users/<uuid:id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_user(id):
    """Update a User for a given id."""
    user_request = request.json

    # Validate request against schema
    try:
        validate(user_request, user_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Retrieve existing user
    user = User.query.get_or_404(str(id))

    # Update user
    user.set_password(user_request["password"])
    user.first_name = user_request["first_name"].title(),
    user.last_name = user_request["last_name"].title(),
    user.email_address = user_request["email_address"].lower()
    user.updated_at = datetime.utcnow()

    # Add children to user
    children = []
    for child_id in user_request["children"]:
        child = Child.query.get(str(child_id))
        if child:
            children.append(child)
        else:
            raise BadRequest("'{0}' is not a valid child ID".format(child_id))
    user.children = children

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


@user.route("/users/<uuid:id>", methods=['DELETE'])
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


@user.route("/login", methods=['POST'])
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

    user = User.query.filter_by(email_address=login_request["email_address"].lower()).first()
    if user is None:
        raise Unauthorized()

    if user.check_password(login_request["password"]):
        user.login_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

        return Response(response=repr(user), mimetype='application/json', status=200)
    else:
        raise Unauthorized()
