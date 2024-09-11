#!/usr/bin/env python3
"""Flask app module"""
from flask import (
    Flask, jsonify, redirect,
    request, abort, make_response, url_for)
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """logs out a user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    """get a user's profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """get a reset password token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
