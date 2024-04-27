#!/usr/bin/python3
"""
View for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""


from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import jsonify, request, abort
from models.place import Place
from models.user import User
from models.amenity import Amenity
from os import getenv


@app_views.route("places/<place_id>/amenities", strict_slashes=False)
def amenity_of_places(place_id):
    """amenity of places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Not found")

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        return [am.to_dict() for am in place.amenities]
    return [am.to_dict() for am in place.amenity_ids]


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def del_post_amenity(pl):
    pass
