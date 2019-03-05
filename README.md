# Diary API

[![Build Status](https://travis-ci.org/MashSoftware/diary-api.svg?branch=master)](https://travis-ci.org/MashSoftware/diary-api)
[![Requirements Status](https://requires.io/github/MashSoftware/diary-api/requirements.svg?branch=master)](https://requires.io/github/MashSoftware/diary-api/requirements/?branch=master)

## Getting started

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=diary_api.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
flask db upgrade
flask run
```

## Routes

### Users

* `POST v1/users` - Create a new user
* `GET v1/users?email_address=<email_address>` - Retrieve a user by email address
* `GET v1/users/<uuid:id>` - Retrieve a specific user
* `PUT v1/users/<uuid:id>/profile` - Update a specific users profile
* `PUT v1/users/<uuid:id>/password` - Update a specific users password
* `DELETE v1/users/<uuid:id>` - Delete a specific user

### Authentication

* `POST v1/login` - Authenticate user credentials

### Children

* `POST v1/children` - Create a new child
* `GET v1/children?user_id=<uuid:user_id>` Retrieve a list of children for a user
* `GET v1/children/<uuid:id>` - Retrieve a specific child
* `PUT v1/children/<uuid:id>` - Update a specific child
* `DELETE v1/children/<uuid:id>` - Delete a specific child

### Events

* `POST v1/children/<uuid:id>/events` - Create a new event for a child
* `GET v1/children/<uuid:id>/events` - Retrieve a list of events for a child
* `GET v1/children/<uuid:id>/events/<uuid:id>` - Retrieve a specific event for a child
* `PUT v1/children/<uuid:id>/events/<uuid:id>` - Update a specific event for a child
* `DELETE v1/children/<uuid:id>/events/<uuid:id>` - Delete a specific event for a child

More details are in the [OpenAPI Specification](openapi.json)

## Event Types

### Point-in-time events

These events occurred at a single point in time. They have a single `occurred_at` attribute set to the a valid [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) formatted timestamp.

* Change

### Period of time events

These events occurred over a period of time. The `started_at` attribute is always set. The `ended_at` attribute may be `null` if the event is currently ongoing, or a valid [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) formatted timestamp if the event has ended.

* Sleep
* Feed

## Event Examples

Example requests to `POST v1/children/<uuid:id>/events` endpoint:

### Sleep

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "sleep",
    "started_at": "2018-07-21T21:21:59.123456",
    "ended_at": null,
    "notes": "Very tired!"
}
```

### Breast feed

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "feed",
    "feed_type": "breast",
    "started_at": "2018-07-21T21:21:59.123456",
    "ended_at": null,
    "side": "left",
    "notes": "Very hungry!"
}
```

### Bottle feed

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "feed",
    "feed_type": "bottle",
    "started_at": "2018-07-21T21:21:59.123456",
    "ended_at": null,
    "amount": 12.5,
    "unit": "ml",
    "notes": "Very hungry!"
}
```

### Formula feed

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "feed",
    "feed_type": "formula",
    "started_at": "2018-07-21T21:21:59.123456",
    "ended_at": null,
    "amount": 12.5,
    "unit": "ml",
    "notes": "Very hungry!"
}
```

### Wet change

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "change",
    "change_type": "wet",
    "occurred_at": "2018-07-21T21:21:59.123456",
    "notes": "Small wee"
}
```

### Soiled change

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "change",
    "change_type": "soiled",
    "occurred_at": "2018-07-21T21:21:59.123456",
    "notes": "Very smelly!"
}
```

### Dry change

Request body:

```json
{
    "user_id": "eac11681-532e-4ec1-8d33-18337485e083",
    "type": "change",
    "change_type": "dry",
    "occurred_at": "2018-07-21T21:21:59.123456",
    "notes": "Clean"
}
```