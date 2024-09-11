#!/usr/bin/env python3
"""End-to-end integration test for user auth service app"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """ tests the user registration endpoint """
    url = f'{BASE_URL}/users'
    data = {'email': email, 'password': password}

    r = requests.post(url, data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}

    r = requests.post(url, data=data)
    assert r.status_code == 400
    assert r.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ tests logging in with a wrong password """
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}

    r = requests.post(url, data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ tests logging in with correct email and password """
    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}

    r = requests.post(url, data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    """ tests getting profile when logged out """
    url = f'{BASE_URL}/profile'
    r = requests.get(url)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ tests getting user profile when logged in """
    url = f'{BASE_URL}/profile'
    r_cookies = {'session_id': session_id}

    r = requests.get(url, cookies=r_cookies)
    assert r.status_code == 200
    assert 'email' in r.json()


def log_out(session_id: str) -> None:
    """ tests logging out a user """
    url = f'{BASE_URL}/sessions'
    r_cookies = {'session_id': session_id}

    r = requests.delete(url, cookies=r_cookies)
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ tests getting a reset password token """
    url = f'{BASE_URL}/reset_password'
    data = {'email': email}

    r = requests.post(url, data=data)
    assert r.status_code == 200
    assert 'email' in r.json()
    assert r.json().get('email') == email
    assert 'reset_token' in r.json()
    return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ tests updating a password """
    url = f'{BASE_URL}/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }

    r = requests.put(url, data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
