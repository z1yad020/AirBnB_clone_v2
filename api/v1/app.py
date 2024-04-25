#!/usr/bin/python3

"""
i dont know what i am doing right know
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def closing(rand):
    storage.close()


@app.errorhandler(404)
def _handle_api_error(ex):
    return {"error": "Not found"}, ex.code


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = "0.0.0.0"
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
