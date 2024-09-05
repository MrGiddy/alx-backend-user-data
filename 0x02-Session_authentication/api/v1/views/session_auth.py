#!/usr/bin/env python3
"""Module of session views"""
from os import getenv
from typing import Tuple, Union
from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Union[str, Tuple[str, int]]:
    """Logs in a user"""
    user_email = request.form.get('email')
    if not user_email or len(user_email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get('password')
    if not user_pwd or len(user_email.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': user_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(user) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = make_response(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """Logs out a user"""
    from api.v1.app import auth

    destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)

    return jsonify({}), 200
