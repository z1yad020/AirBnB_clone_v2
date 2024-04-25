#!/usr/bin/python3

"""
what am i doing
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes_stat = {
        'users': User, 'places': Place,
        'states': State, 'cities': City, 'amenities': Amenity,
        'reviews': Review
        }


@app_views.route("/status")
def status():
    """show api status"""
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    stat = {}

    for key, value in classes_stat.items():
        stat[key] = storage.count(value)

    return stat
