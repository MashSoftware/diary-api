import json
from datetime import date, datetime

from flask import Blueprint, Response, request, url_for
from flask_negotiate import consumes, produces
from jsonschema import FormatChecker, ValidationError, validate
from werkzeug.exceptions import BadRequest, NotImplemented

from app import db
from app.models import Child, Event, User

child = Blueprint('child', __name__)

# JSON schema for child requests
with open('openapi.json') as json_file:
    openapi = json.load(json_file)
child_schema = openapi["components"]["schemas"]["ChildRequest"]
event_schema = openapi["components"]["schemas"]["EventRequest"]


@child.route("", methods=['GET'])
@produces('application/json')
def get_children():
    """Get Children for a given User ID"""
    user_query = request.args.get('user_id', type=str)
    result = []

    if user_query is not None:
        user = User.query.get_or_404(user_query)
        for child in user.children:
            result.append(child.as_dict())
    else:
        raise BadRequest("'user_id' is a required query parameter")

    return Response(response=json.dumps(result, sort_keys=True, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@child.route("", methods=['POST'])
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

    if date.fromisoformat(child_request["date_of_birth"]) > date.today():
        raise BadRequest('Date of birth must be in the past')

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
            raise BadRequest("'{0}' is not a valid user ID".format(user_id))
    child.users = users

    # Commit child to db
    db.session.add(child)
    db.session.commit()

    # Create response
    response = Response(response=repr(child), mimetype='application/json', status=201)
    response.headers["Location"] = url_for('child.get_child', child_id=child.id)

    return response


@child.route("/<uuid:child_id>", methods=['GET'])
@produces('application/json')
def get_child(child_id):
    """Get a Child for a given ID."""
    child = Child.query.get_or_404(str(child_id))

    return Response(response=repr(child),
                    mimetype='application/json',
                    status=200)


@child.route("/<uuid:child_id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_child(child_id):
    """Update a Child for a given ID."""
    child_request = request.json

    # Validate request against schema
    try:
        validate(child_request, child_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise BadRequest(e.message)

    # Retrieve existing child
    child = Child.query.get_or_404(str(child_id))

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
            raise BadRequest("'{0}' is not a valid user ID".format(user_id))
    child.users = users

    # Commit child to db
    db.session.add(child)
    db.session.commit()

    return Response(response=repr(child),
                    mimetype='application/json',
                    status=200)


@child.route("/<uuid:child_id>", methods=['DELETE'])
@produces('application/json')
def delete_child(child_id):
    """Delete a Child for a given ID."""
    child = Child.query.get_or_404(str(child_id))

    db.session.delete(child)
    db.session.commit()
    return Response(response=None,
                    mimetype='application/json',
                    status=204)


@child.route("/<uuid:child_id>/events", methods=['GET'])
@produces('application/json')
def get_events(child_id):
    """Get Events for a Child."""
    events = Event.query.filter_by(child_id=str(child_id)).order_by(Event.started_at.desc()).all()
    result = []
    for event in events:
        result.append(event.as_dict())

    return Response(response=json.dumps(result, sort_keys=True, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@child.route("/<uuid:child_id>/events", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_event(child_id):
    """Create a new Event."""
    event_request = request.json

    # Validate request against schema
    # try:
    #     validate(event_request, event_schema, format_checker=FormatChecker())
    # except ValidationError as e:
    #     raise BadRequest(e.message)

    # Create a new event object
    event = Event(
        user_id=event_request["user_id"],
        child_id=str(child_id),
        type=event_request["type"],
        started_at=event_request["started_at"]
    )

    event.ended_at = event_request["ended_at"] if "ended_at" in event_request else None
    event.feed_type = event_request["feed_type"] if "feed_type" in event_request else None
    event.change_type = event_request["change_type"] if "change_type" in event_request else None
    event.amount = event_request["amount"] if "amount" in event_request else None
    event.unit = event_request["unit"] if "unit" in event_request else None
    event.side = event_request["side"] if "side" in event_request else None
    event.notes = event_request["notes"] if "notes" in event_request else None

    # Commit event to db
    db.session.add(event)
    db.session.commit()

    # Create response
    response = Response(response=repr(event), mimetype='application/json', status=201)
    response.headers["Location"] = url_for('child.get_event', child_id=child_id, event_id=event.id)

    return response


@child.route("/<uuid:child_id>/events/<uuid:event_id>", methods=['GET'])
@produces('application/json')
def get_event(child_id, event_id):
    """Get an Event for a given ID."""
    raise NotImplemented()


@child.route("/<uuid:child_id>/events/<uuid:event_id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_event(child_id, event_id):
    """Update a Event for a given ID."""
    event_request = request.json

    # Validate request against schema
    # try:
    #     validate(event_request, event_schema, format_checker=FormatChecker())
    # except ValidationError as e:
    #     raise BadRequest(e.message)

    # Retrieve existing event
    event = Event.query.get_or_404(str(event_id))

    # Update event
    event.user_id = event_request["user_id"]
    event.type = event_request["type"]
    event.started_at = event_request["started_at"]
    event.ended_at = event_request["ended_at"] if "ended_at" in event_request else None
    event.feed_type = event_request["feed_type"] if "feed_type" in event_request else None
    event.change_type = event_request["change_type"] if "change_type" in event_request else None
    event.amount = event_request["amount"] if "amount" in event_request else None
    event.unit = event_request["unit"] if "unit" in event_request else None
    event.side = event_request["side"] if "side" in event_request else None
    event.notes = event_request["notes"] if "notes" in event_request else None
    event.updated_at = datetime.utcnow()

    # Commit event to db
    db.session.add(event)
    db.session.commit()

    return Response(response=repr(event),
                    mimetype='application/json',
                    status=200)


@child.route("/<uuid:child_id>/events/<uuid:event_id>", methods=['DELETE'])
@produces('application/json')
def delete_event(child_id, event_id):
    """Delete a Event for a given ID."""
    event = Event.query.get_or_404(str(event_id))

    db.session.delete(event)
    db.session.commit()
    return Response(response=None,
                    mimetype='application/json',
                    status=204)
