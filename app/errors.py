import json

from flask import Response
from werkzeug.exceptions import HTTPException

from app import app


@app.errorhandler(HTTPException)
def bad_request(error):
    return Response(response=json.dumps({"description": error.description}, separators=(',', ':')),
                    mimetype='application/json',
                    status=error.code)
