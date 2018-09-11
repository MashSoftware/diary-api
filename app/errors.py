from flask import Response

from app import app


@app.errorhandler(404)
def not_found(error):
    return Response(response='{"message":"Not found"}',
                    mimetype='application/json',
                    status=404)


@app.errorhandler(500)
def internal_server(error):
    return Response(response='{"message":"Internal server error"}',
                    mimetype='application/json',
                    status=500)
