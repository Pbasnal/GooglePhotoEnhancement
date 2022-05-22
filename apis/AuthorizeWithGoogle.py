import os
import google
import google_auth_oauthlib.flow
import config

from app import db, app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, session, request
from flask_restful import Resource, Api
from gphotospy import authorize


def getAuthorizedService():
    try:
        if not os.path.exists(config.CLIENT_SECRET_FILE):
            with open(config.CLIENT_SECRET_FILE, "w") as f:
                f.write(os.environ[config.CLIENT_SECRET_ENV])

        return authorize.init(config.CLIENT_SECRET_FILE)
    except:
        if os.path.exists("photoslibrary_v1.token"):
            os.remove("photoslibrary_v1.token")
    return authorize.init(config.CLIENT_SECRET_FILE)

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        config.CLIENT_SECRET_FILE, scopes=config.SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    googlesession = flow.authorized_session()
    userInfo = googlesession.get('https://www.googleapis.com/userinfo/v2/me')

    from UserAuth import UserOauth

    newUser = UserOauth.createUserObject(userInfo.json(), credentials)
    db.session.add(newUser)
    db.session.commit()

    session['user_id'] = newUser.id

    return redirect(url_for('helloworld'))
    
def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

class AuthorizeWithGoogle(Resource):
    def get(self):
        authorization_url = self.authorize()
        return redirect(authorization_url)

    def authorize(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            config.CLIENT_SECRET_FILE, scopes=config.SCOPES)

        flow.redirect_uri = url_for('oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        # Store the state so the callback can verify the auth server response.
        session['state'] = state

        return authorization_url



def credentials_from_user(user):
    scopes = []
    for scope in user.scopes.split(','):
        scope = 'https://www.googleapis.com/auth/' + scope
        scopes.append(scope)

    return google.oauth2.credentials.Credentials(
        user.token,
        refresh_token=user.refresh_token,
        token_uri=user.token_uri,
        client_id=user.client_id,
        client_secret=user.client_secret)

    # return {'token': user.token,
    #         'refresh_token': user.refresh_token,
    #         'token_uri': user.token_uri,
    #         'client_id': user.client_id,
    #         'client_secret': user.client_secret,
    #         'scopes': scopes}