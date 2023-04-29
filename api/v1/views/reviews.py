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
from models.place import Place
from models.user import User


@app_views.route('/places/<p>/reviews', methods=['GET'], strict_slashes=False)
def all_reviews(p):
    """Retrieves all the review objects"""
    places = storage.get("Place", p)
    if places is None:
        abort(404)

    lis = []
    for review in places.reviews:
        lis.append(review.to_dict())
    return jsonify(lis)


@app_views.route('/reviews/<rv>', methods=['GET'], strict_slashes=False)
def review_id(rv):
    """Retrieves the review obj from database else raises an error"""
    review = storage.get("Review", rv)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<rv>', methods=['DELETE'], strict_slashes=False)
def delete_review(rv):
    """deletes reviews associated with place and returns an empty object\
            if found else raises a 404 error."""
    review = storage.get('Review', rv)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<rv>', methods=['PUT'], strict_slashes=False)
def put_review(rv):
    """Updates the database based on the reviews of a place"""
    review = storage.get('Review', rv)
    if review is None:
        abort(404)

    if not request.json:
        abort(404, "Not a JSON")

    ignore = ['id', 'created_at', 'user_id', 'place_id', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200


@app_views.route('/places/<p>/reviews', methods=['POST'], strict_slashes=False)
def post_review(p):
    """Creates a new review of a place"""
    if not request.json:
        abort(404, "Not a JSON")


    if 'user_id' not in request.json.keys():
        abort(404, "Missing user_id")

    if 'text' not in request.json.keys():
        abort(404, "Missing text")

    place = storage.get('Place', p)
    if place is None:
        abort(404)

    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)

    review = Review(**request.json)
    review.user_id = user.id
    review.place_id = place.id
    review.save()
    return jsonify(review.to_dict()), 201
