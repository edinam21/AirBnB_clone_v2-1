#!/usr/bin/python3
"""
Contains routes for all the objects.
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def custom_404(error):
    """handles bad request 404"""
    return jsonify(error="Not found")


@app.teardown_appcontext
def close(exception):
    """closes the connection to database"""
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
