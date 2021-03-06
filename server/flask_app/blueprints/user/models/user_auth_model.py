import json
from loguru import logger
from flask_app.sqldb.appdb import db


class UserOauth(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    verified_email = db.Column(db.Boolean, default=False, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(200), nullable=False)
    locale = db.Column(db.String(5), nullable=False)

    token = db.Column(db.String(200), unique=True, nullable=False)
    refresh_token = db.Column(db.String(200), unique=True, nullable=False)
    token_uri = db.Column(db.String(100), unique=False, nullable=False)
    client_id = db.Column(db.String(150), unique=True, nullable=False)
    client_secret = db.Column(db.String(150), unique=False, nullable=False)
    # Add prefix https://www.googleapis.com/auth/ to the scopes.
    # Scopes will be a comma separated list.
    scopes = db.Column(db.String(150), unique=False, nullable=False)
    is_valid = db.Column(db.Boolean, default=True, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,

            "email": self.email,
            "verified_email": self.verified_email,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale,

            'token': self.token,
            'refresh_token': self.refresh_token,
            'token_uri': self.token_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scopes': self.scopes
        }

    def createUserObject(userInfo, credentials):

        newUserOauth = UserOauth(
            id=userInfo["id"],
            email=userInfo["email"],
            verified_email=userInfo["verified_email"],
            name=userInfo["name"],
            given_name=userInfo["given_name"],
            family_name=userInfo["family_name"],
            picture=userInfo["picture"],
            locale=userInfo["locale"],
        )
        newUserOauth.updateUserTokens(credentials)

        return newUserOauth

    def updateUserTokens(self, credentials):
        self.token = credentials.token
        self.refresh_token = credentials.refresh_token
        self.token_uri = credentials.token_uri
        self.client_id = credentials.client_id
        self.client_secret = credentials.client_secret

        scopes = []
        for scope in credentials.scopes.split(' '):
            scope = scope.replace('https://www.googleapis.com/auth/', '')
            scopes.append(scope)

        self.scopes = ",".join(scopes)
        logger.debug("logging scopes - " + self.scopes)

    def getUser(userId):
        getUserQuery = UserOauth.query.filter(UserOauth.id == userId)
        if getUserQuery.first() is None:
            return None

        return UserOauth.query.filter(UserOauth.id == userId).one()

    def email_exists(verified_email):
        return UserOauth.query.filter_by(verified_email=verified_email).first() is not None
