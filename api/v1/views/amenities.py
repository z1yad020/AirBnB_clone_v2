#!/usr/bin/python3

"""
View for Amenity objects that handles all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """all amenties"""
    if request.method == 'GET':
        objs = storage.all(Amenity).values()
        if objs is None:
            abort(404)
        return [obj.to_dict() for obj in objs]

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            name = data["name"]
        except Exception:
            abort(400, "Missing name")

        am = Amenity(name=name)
        am.save()
        return am.to_dict(), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity_by_id(amenity_id):
    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)

    if request.method == 'GET':
        return amenity.to_dict()

    elif request.method == 'DELETE':
        storage.delete(am)
        storage.save()
        return {}, 200

    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ("id",
                       "created_at",
                       "updated_at") and am.__dict__.get(key) is not None:
            setattr(am, key, value)
        storage.save()
        return amenity.to_dict(), 200
