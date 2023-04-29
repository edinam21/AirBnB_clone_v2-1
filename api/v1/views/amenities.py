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
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves all the amenity objects"""
    obj = storage.all("Amenity")
    lis = []
    for value in obj.values():
        lis.append(value.to_dict())
    return jsonify(lis)


@app_views.route('/amenities/<a_id>', methods=['GET'], strict_slashes=False)
def state_id(a_id):
    """Retrieves the state id from database else raises an error"""
    amenity = storage.get("Amenity", a_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<a_d>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_id(a_d):
    """deletes a state object and returns an empty object\
            if found else raises a 404 error."""
    amenity = storage.get('Amenity', a_d)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<a_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(a_id):
    """Updates the database based on the state object"""
    amenity = storage.get('Amenity', a_id)
    if amenity is None:
        abort(404)

    if not request.json:
        abort(404, "Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post():
    """Creates a new post"""
    if not request.json:
        abort(404, "Not a JSON")

    if 'name' not in request.json.keys():
        abort(404, "Missing name")

    amenity = Amenity(**request.json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201
