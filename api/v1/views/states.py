#!/usr/bin/python3

"""
View for State objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes = False)
@app_views.route("/states/<state_id>", strict_slashes = False)
def all_states(state_id = None):
    """all states"""
    if state_id is None:
        objs = storage.all(State).values()
        return [ob.to_dict() for ob in objs]

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return obj.to_dict()
