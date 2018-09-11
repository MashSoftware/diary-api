from flask import Response

from app import app


@app.errorhandler(400)
def bad_request(error):
    return Response(response='{"message":"Bad request"}',
                    mimetype='application/json',
                    status=400)


@app.errorhandler(404)
def not_found(error):
    return Response(response='{"message":"Not found"}',
                    mimetype='application/json',
                    status=404)


@app.errorhandler(405)
def method_not_allowed(error):
    return Response(response='{"message":"Method not allowed"}',
                    mimetype='application/json',
                    status=405)


@app.errorhandler(406)
def not_acceptable(error):
    return Response(response='{"message":"Not acceptable"}',
                    mimetype='application/json',
                    status=406)


@app.errorhandler(415)
def unsupported_media_type(error):
    return Response(response='{"message":"Unsupported media type"}',
                    mimetype='application/json',
                    status=415)


@app.errorhandler(429)
def too_many_requests(error):
    return Response(response='{"message":"Too many requests"}',
                    mimetype='application/json',
                    status=429)


@app.errorhandler(500)
def internal_server(error):
    return Response(response='{"message":"Internal server error"}',
                    mimetype='application/json',
                    status=500)
