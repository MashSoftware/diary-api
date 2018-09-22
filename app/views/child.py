import json
from datetime import datetime

from flask import Blueprint, Response, request
from flask_negotiate import consumes, produces
from werkzeug.exceptions import BadRequest

from app import db
from app.models import Child, User
from jsonschema import FormatChecker, ValidationError, validate

child = Blueprint('child', __name__)

# JSON schema for child requests
with open('openapi.json') as json_file:
    openapi = json.load(json_file)
child_schema = openapi["components"]["schemas"]["ChildRequest"]


@child.route("/children", methods=['GET'])
@produces('application/json')
def get_children():
    """Get Children."""
    children = Child.query.order_by(Child.created_at).all()
    result = []
    for child in children:
        result.append(child.as_dict())

    return Response(response=json.dumps(result, sort_keys=True, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@child.route("/children", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_child():
    """Create a new Child."""
    child_request = request.json

    # Validate request against schema
    try:
        validate(child_request, child_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Create a new child object
    child = Child(
        first_name=child_request["first_name"],
        last_name=child_request["last_name"],
        date_of_birth=child_request["date_of_birth"]
    )

    # Add user to child
    users = []
    for user_id in child_request["users"]:
        user = User.query.get(str(user_id))
        if user:
            users.append(user)
        else:
            raise BadRequest()
    child.users = users

    # Commit child to db
    db.session.add(child)
    db.session.commit()

    # Create response
    response = Response(response=repr(child), mimetype='application/json', status=201)
    response.headers["Location"] = "{0}/{1}".format(request.url, child.id)

    return response


@child.route("/children/<uuid:id>", methods=['GET'])
@produces('application/json')
def get_child(id):
    """Get a Child for a given id."""
    child = Child.query.get_or_404(str(id))

    return Response(response=repr(child),
                    mimetype='application/json',
                    status=200)


@child.route("/children/<uuid:id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_child(id):
    """Update a Child for a given id."""
    child_request = request.json

    # Validate request against schema
    try:
        validate(child_request, child_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Retrieve existing child
    child = Child.query.get_or_404(str(id))

    # Update child
    child.first_name = child_request["first_name"].title(),
    child.last_name = child_request["last_name"].title(),
    child.date_of_birth = child_request["date_of_birth"],
    child.updated_at = datetime.utcnow()

    # Add user to child
    users = []
    for user_id in child_request["users"]:
        user = User.query.get(str(user_id))
        if user:
            users.append(user)
        else:
            raise BadRequest()
    child.users = users

    # Commit child to db
    db.session.add(child)
    db.session.commit()

    return Response(response=repr(child),
                    mimetype='application/json',
                    status=200)


@child.route("/children/<uuid:id>", methods=['DELETE'])
@produces('application/json')
def delete_child(id):
    """Delete a Child for a given id."""
    child = Child.query.get_or_404(str(id))

    db.session.delete(child)
    db.session.commit()
    return Response(response=None,
                    mimetype='application/json',
                    status=204)
