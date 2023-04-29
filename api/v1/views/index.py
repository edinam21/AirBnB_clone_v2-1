#!/usr/bin/python3
"""Contains the routes for the json objects
Routes:
    /status: returns the 'OK' status
    /stats: returns the total count of the objects in database
Usage:
    ./app
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def static():
    """returns json object"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns the count for all items in database"""
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    obj = {
            'amenities': amenities,
            'cities': cities,
            'places': places,
            'reviews': reviews,
            'states': states,
            'users': users
            }
    return jsonify(obj)
