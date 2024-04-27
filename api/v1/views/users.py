#!/usr/bin/python3

"""View for Cities"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import request, abort


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    if request.method == 'GET':
        users = storage.all(User).values()
        return [user.to_dict() for user in users]
    elif request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if "email" not in data.keys():
            abort(400, "Missing email")
        elif "password" not in data.keys():
            abort(400, "Missing password")
        user = User(**data)
        storage.save()
        return user.to_dict(), 201


@app_views.route('users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_by_id(user_id):
    user = storage.get(User, user_id)
    if not user:
        return abort(404, "Not found")
    if request.method == 'GET':
        return user.to_dict()
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return {}, 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ("id", "email", "created_at", "updated_at"):
                setattr(user, key, value)
        storage.save()
        return user.to_dict(), 200
