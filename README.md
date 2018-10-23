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

* `POST /users` - Create a new user
* `GET /users?email_address=<email_address>` - Retrieve a user by email address
* `GET /users/<uuid:id>` - Retrieve a specific user
* `PUT /users/<uuid:id>/profile` - Update a specific users profile
* `PUT /users/<uuid:id>/password` - Update a specific users password
* `DELETE /users/<uuid:id>` - Delete a specific user

### Authentication

* `POST /login` - Authenticate user credentials

### Children

* `POST /children` - Create a new child
* `GET /children?user_id=<uuid:user_id>` Retrieve a list of children for a user
* `GET /children/<uuid:id>` - Retrieve a specific child
* `PUT /children/<uuid:id>` - Update a specific child
* `DELETE /children/<uuid:id>` - Delete a specific child

### Events

* `POST /children/<uuid:id>/events` - Create a new event for a child
* `GET /children/<uuid:id>/events` - Retrieve a list of events for a child
* `PUT /children/<uuid:id>/events/<uuid:id>` - Update a specific event for a child
* `DELETE /children/<uuid:id>/events/<uuid:id>` - Delete a specific event for a child

More details are in the [OpenAPI Specification](openapi.json)