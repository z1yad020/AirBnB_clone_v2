#!/usr/bin/python3

"""
View for State objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def all_states(state_id=None):
    """all states"""
    if state_id is None:
        objs = storage.all(State).values()
        return [ob.to_dict() for ob in objs]

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/states/<state_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    obj = storage.get(State, state_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    try:
        name = data["name"]
    except Exception:
        abort(400, "Missing name")

    obj = State(name=name)
    obj.save()
    return obj.to_dict(), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ("id", "created_at",
                "updated_at") and obj.__dict__.get(key) is not None:
            setattr(obj, key, value)

    obj.save()
    return obj.to_dict(), 201
