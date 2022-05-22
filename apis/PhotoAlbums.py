from flask_restful import Resource
from flask import make_response, redirect, render_template, session, request, url_for
from photoEnhancer import loadListOfAlbumsFromCache

from apis.AuthorizeWithGoogle import getGooglePhotoService

class PhotoAlbums(Resource):
    def __init__(self, api):
        self.__name__ = "photoalbums"
        self.api = api

    def get(self):
        if 'user_id' not in session:
            return "User not found", 400
        googleService = getGooglePhotoService(session["user_id"])

        if googleService == None:
            return "failed to create google service", 500
        albumIdMap = loadListOfAlbumsFromCache(googleService)
        if bool(albumIdMap) == False:
            print(f"No album Id to process photos of")

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("albums/albums.html", albums=albumIdMap), 200, headers)

    def post(self):
        # json_data = request.get_json(force=True)

        if request.form is None \
            or len(request.form) == 0 \
            or "albumId" not in request.form:

            return redirect(self.api.url_for(PhotoAlbums))
    

        print(request.form["albumId"])

        return redirect(self.api.url_for(PhotoAlbums))