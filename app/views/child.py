import json

from flask import Blueprint, Response, request
from flask_negotiate import consumes, produces
from werkzeug.exceptions import BadRequest

from app import db
from app.models import Child, User

child = Blueprint('child', __name__)


@child.route("/children", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_child():
    """Create a new Child."""
    child_request = request.json

    # Create a new child object
    child = Child(
        first_name=child_request["first_name"],
        last_name=child_request["last_name"],
        date_of_birth=child_request["date_of_birth"]
    )

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


@child.route("/children/<uuid:id>", methods=['GET'])
@produces('application/json')
def get_child(id):
    """Get a Child for a given ID."""
    child = Child.query.get_or_404(str(id))

    return Response(response=repr(child),
                    mimetype='application/json',
                    status=200)
