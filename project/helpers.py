import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def searchCity(searched):
    """find a latitude/longitude by city"""
    # contact API
    try:
        map_api_key = "GAgKijg1HVt2u1uFp7OoUlJzdQvSZGAt"
        response = requests.get(f"http://open.mapquestapi.com/geocoding/v1/address?key={map_api_key}&location={searched}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        info = response.json()
        return info["results"][0]["locations"][0]["latLng"]
    except (KeyError, TypeError, ValueError):
        return None

def searchHike(lat, lng):
    try:
        hiking_api_key = "200899971-312e95626d1a9525111ec53cb3d9fbf6"
        response = requests.get(f"https://www.hikingproject.com/data/get-trails?lat={lat}&lon={lng}&maxDistance=50&maxResults=500&key={hiking_api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None
    # Parse response
    try:
        hikes = response.json()
        return hikes
    except (KeyError, TypeError, ValueError):
        return None


