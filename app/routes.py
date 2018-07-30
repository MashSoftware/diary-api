import json
from datetime import datetime

import bcrypt
from app import app, db
from app.models import Child, User
from flask import Response, request
from flask_negotiate import consumes, produces


@app.route("/users", methods=['GET'])
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


@app.route("/users", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_user():
    """Create a new User."""
    user_request = request.json

    # Create a new user object
    user = User(
        password=user_request["password"],
        first_name=user_request["first_name"],
        last_name=user_request["last_name"],
        email_address=user_request["email_address"]
    )

    # Commit user to db
    db.session.add(user)
    db.session.commit()

    # Create response
    response = Response(response=repr(user), mimetype='application/json', status=201)
    response.headers["Location"] = "{0}/{1}".format(request.url, user.user_id)

    return response


@app.route("/users/<uuid:user_id>", methods=['GET'])
@produces('application/json')
def get_user(user_id):
    """Get a User for a given user_id."""
    user = User.query.get_or_404(str(user_id))

    return Response(response=repr(user),
                    mimetype='application/json',
                    status=200)


@app.route("/users/<uuid:user_id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_user(user_id):
    """Update a User for a given user_id."""
    user_request = request.json

    # Retrieve existing user
    user = User.query.get_or_404(str(user_id))

    # Update user
    user.password = bcrypt.hashpw(user_request["password"].encode('UTF-8'), bcrypt.gensalt())
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
    user.children = children

    # Commit user to db
    db.session.add(user)
    db.session.commit()

    return Response(response=repr(user),
                    mimetype='application/json',
                    status=200)


@app.route("/users/<uuid:user_id>", methods=['DELETE'])
@produces('application/json')
def delete_user(user_id):
    """Delete a User for a given user_id."""
    user = User.query.get_or_404(str(user_id))

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
