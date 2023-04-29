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
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves all the state objects"""
    obj = storage.all("State")
    lis = []
    for value in obj.values():
        lis.append({
            '__class__': 'State',
            'created_at': value.created_at.isoformat(),
            'id': value.id,
            'name': value.name,
            'updated_at': value.updated_at.isoformat()})
    return jsonify(lis)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def all_state_id(state_id):
    """Retrieves the state id from database else raises an error"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    return jsonify({
        '__class__': 'State',
        'created_at': state.created_at.isoformat(),
        'id': state.id,
        'name': state.name,
        'updated_at': state.updated_at.isoformat()})


@app_views.route('/states/<sta_id>', methods=['DELETE'], strict_slashes=False)
def delete_status_id(sta_id):
    """deletes a state object and returns an empty object\
            if found else raises a 404 error."""
    states = storage.get('State', sta_id)
    if states is None:
        abort(404)

    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates the database based on the state object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if not request.json:
        abort(404, "Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(state, key, value)

    state.save()

    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new post"""
    if not request.json:
        abort(404, "Not a JSON")


    if 'name' not in request.json.keys():
        abort(404, "Missing name")

    state = State(**request.json)
    state.save()
    return jsonify(state.to_dict()), 201
