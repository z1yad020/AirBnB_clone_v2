#!/usr/bin/python3

"""
View for City objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def all_cities_of_state(state_id):
    """all cities of state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    return [ct.to_dict() for ct in obj.cities]


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    obj = storage.get(City, city_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    try:
        name = data["name"]
    except Exception:
        abort(400, "Missing name")

    ct = City(state_id=state_id, name=name)
    ct.save()
    return ct.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ("id",
                       "created_at",
                       "updated_at",
                       "state_id") and obj.__dict__.get(key) is not None:
            setattr(obj, key, value)

    obj.save()
    return obj.to_dict(), 200
