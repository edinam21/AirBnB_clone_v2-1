#!/usr/bin/python3
'''Routes for the state object.
Routes:
    /states: gets all the state objects
    /states/<state_id>: gets a specific state object matching the id
    /states/<sta_id>: deletes a specific state object matching id
    /states/<state_id>: posts a new state object
    /states/<state_id>: updates a specific state object
'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves all the state objects"""
    users = storage.all("User")
    lis = []
    for user in users.values():
        lis.append(user.to_dict())
    return jsonify(lis)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """Retrieves the user id from database else raises an error"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_id(user_id):
    """deletes a user object and returns an empty object\
            if found else raises a 404 error."""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates the database based on the user object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if not request.json:
        abort(404, "Not a JSON")

    ignore = ['id', 'created_at', 'email', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new post"""
    if not request.json:
        abort(404, "Not a JSON")

    if 'email' not in request.json.keys():
        abort(404, "Missing email")

    if 'password' not in request.json.keys():
        abort(404, "Missing password")


    user = User(**request.json)
    user.save()
    return jsonify(user.to_dict()), 201
