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
* `PUT v1/children/<uuid:id>/events/<uuid:id>` - Update a specific event for a child
* `DELETE v1/children/<uuid:id>/events/<uuid:id>` - Delete a specific event for a child

More details are in the [OpenAPI Specification](openapi.json)