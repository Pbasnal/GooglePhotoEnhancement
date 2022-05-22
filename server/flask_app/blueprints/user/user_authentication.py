from ast import arg
import json
import os

from requests import get
import flask_app.blueprints.user.config as config

import google_auth_oauthlib.flow

from functools import wraps
from flask import Blueprint, redirect, url_for, session, request

from flask_app.blueprints.user.models.user_auth_model import UserOauth
from flask_app.sqldb.appdb import db
from flask_app.applogger import logger


bp = Blueprint('user_auth', __name__, url_prefix='/user_auth')

USER_ID_SESSION_KEY = "user_id"
USER_STATE_SESSION_KEY = "state"


def login_is_required(function):
    @wraps(function)
    def wrapper(**kargs):
        user = get_logged_in_user()
        if user is None:
            return redirect(url_for("user_auth.authorize"))

        logger.info(f"Logged in function: {user} {kargs}")
        if kargs is not None and len(kargs.keys()) > 0:
            return function(user, kargs)
        return function(user)

    return wrapper


def get_logged_in_user() -> UserOauth:
    if USER_ID_SESSION_KEY not in session:
        return None

    return UserOauth.getUser(session[USER_ID_SESSION_KEY])


@bp.route('/')
def authorize():
    logger.debug(f"Secret file location: {os.getcwd()}")
    logger.debug(f"Data in session: {session}")

    user = get_logged_in_user()
    if user is not None:
        logger.info(f"User is logged in already: {user.serialize}")
        return user.serialize

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        config.CLIENT_SECRET_FILE, scopes=config.SCOPES)

    flow.redirect_uri = url_for('user_auth.oauth2_callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session[USER_STATE_SESSION_KEY] = state

    return redirect(authorization_url)

@bp.route('/<user_id>')
def get_user_token(user_id):
    logger.debug(UserOauth.getUser(user_id))
    return UserOauth.getUser(user_id).serialize

@bp.route('/all_users')
def get_all_users():
    return json.dumps([user.serialize for user in UserOauth.query.all()])

@bp.route("/logout")
@login_is_required
def logout_user(user):
    session[USER_ID_SESSION_KEY] = None
    session[USER_STATE_SESSION_KEY] = None

    return redirect("/")


@bp.route('/oauth2callback')
def oauth2_callback():
    flow = get_oauth_flow()
    # store_oauth_credentials_in_session(flow)

    credentials = flow.credentials
    userInfo = get_user_info(flow)
    if userInfo == None:
        logger.error(f"Didn't recieve any user info in the oauth callback")
        return "Didn't recieve any user info in the oauth callback"

    if UserOauth.email_exists(userInfo['verified_email']):
        user = UserOauth.getUser(userInfo["id"])
        user.updateUserTokens(credentials)
    else:
        user = UserOauth.createUserObject(userInfo, credentials)
        db.session.add(user)

    db.session.commit()

    session[USER_ID_SESSION_KEY] = user.id

    return redirect(url_for('user_is_logged_in'))


def get_user_info(flow):
    googlesession = flow.authorized_session()
    userInfo = googlesession.get('https://www.googleapis.com/userinfo/v2/me')
    if userInfo == None:
        return None

    return userInfo.json()


# def store_oauth_credentials_in_session(flow):
#     # Store credentials in the session.
#     credentials = flow.credentials
#     session['credentials'] = credentials_to_dict(credentials)


def get_oauth_flow():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session[USER_STATE_SESSION_KEY]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        config.CLIENT_SECRET_FILE, scopes=config.SCOPES, state=state)
    flow.redirect_uri = url_for('user_auth.oauth2_callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    return flow


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
