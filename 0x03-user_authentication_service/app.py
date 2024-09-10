#!/usr/bin/env python3
"""Flask app module"""
from flask import (Flask, jsonify, request, abort, make_response)
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """home page route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """register a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    # catch ValueError raised if user exists
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login():
    """log in a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    authenticated = AUTH.valid_login(email, password)
    if not authenticated:
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
