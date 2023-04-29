#!/usr/bin/python3
'''Routes for the state object.
Routes:
    /cities: gets all the state objects
    /s/<state_id>: gets a specific state object matching the id
    /states/<sta_id>: deletes a specific state object matching id
    /states/<state_id>: posts a new state object
    /states/<state_id>: updates a specific state object
'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<cd>/places', methods=['GET'], strict_slashes=False)
def all_places(cd):
    """Retrieves all the place objects"""
    cities = storage.get("City", cd)
    if cities is None:
        abort(404)

    lis = []
    for place in cities.places:
        lis.append(place.to_dict())
    return jsonify(lis)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """Retrieves the place id from database else raises an error"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<p_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_id(p_id):
    """deletes a place object and returns an empty object\
            if found else raises a 404 error."""
    place = storage.get('Place', p_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates the database based on the place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(404, "Not a JSON")

    ignore = ['id', 'created_at', 'user_id', 'city_id', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<c>/places', methods=['POST'], strict_slashes=False)
def post_place(c):
    """Creates a new place"""
    if not request.json:
        abort(404, "Not a JSON")


    if 'user_id' not in request.json.keys():
        abort(404, "Missing user_id")

    if 'name' not in request.json.keys():
        abort(404, "Missing name")

    city = storage.get('City', c)
    if city is None:
        abort(404)

    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)

    place = Place(**request.json)
    place.city_id = city.id
    place.user_id = user.id
    place.save()
    return jsonify(place.to_dict()), 201
