#!/usr/bin/python3

"""
what am i doing
"""

from api.v1.views import app_views

@app_views.route("/status")
def status():
    """show api status"""
    return {"status":"OK"}
