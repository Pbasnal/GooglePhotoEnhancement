from flask_restful import Resource
from flask import make_response, redirect, render_template, session, request, url_for
from photoEnhancer import loadListOfAlbumsFromCache
from googleapiclient.discovery import build

from app import api
import config
import google


class PhotoAlbums(Resource):
    def get(self):
        if 'user_id' not in session:
            return "User not found", 400
        googleService = self.getGooglePhotoService(session["user_id"])

        if googleService == None:
            return "failed to create google service", 500
        albumIdMap = loadListOfAlbumsFromCache(googleService)
        if bool(albumIdMap) == False:
            albumIdMap = loadListOfAlbumsFromCache(googleService, True)

        if bool(albumIdMap) == False:
            print(f"No album Id to process photos of")

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("albums/albums.html", albums=albumIdMap), 200, headers)

    def post(self):
        # json_data = request.get_json(force=True)

        if request.form is None \
            or len(request.form) == 0 \
            or "albumId" not in request.form:

            return redirect(api.url_for(PhotoAlbums))
    

        print(request.form["albumId"])

        return redirect(api.url_for(PhotoAlbums))

    def getGooglePhotoService(self, userId):

        from UserAuth import UserOauth

        user = UserOauth.query.filter(UserOauth.id == userId).one()
        service_object = {
            "secrets": config.CLIENT_SECRET_FILE
        }
        credentials = self.credentials_from_user(user)
        try:
            service = build(config.API_SERVICE_NAME, config.API_VERSION,
                            static_discovery=False, credentials=credentials)
            service_object["service"] = service
            return service_object
        except Exception as e:
            print(e)
        return None

    def credentials_from_user(self, user):
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
