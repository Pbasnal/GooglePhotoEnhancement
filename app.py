from logging import debug
from flask import Flask, request
from flask_restful import Resource, Api
from GoogleMediaItem import GoogleMediaItem
from gphotospy import authorize
import os
from loadalbums import getAllAlbumsFromGoogle
from photoEnhancer import loadListOfAlbumsFromCache

app = Flask(__name__)
api = Api(app)


DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"
PROCESSED_FOLDER = "DPED/dped/iphone/test_data"
CLIENT_SECRET_FILE = "google_web_secret.json"

def getAuthorizedService():  
    try:
        return authorize.init(CLIENT_SECRET_FILE)
    except :
        os.remove("photoslibrary_v1.token")
    return authorize.init(CLIENT_SECRET_FILE)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

class AuthorizeWithGoogle(Resource):
    def get(self):
        return getAuthorizedService()

class PhotoAlbums(Resource):
    def get(self):
        googleService = getAuthorizedService()
        albumIdMap = loadListOfAlbumsFromCache(googleService)
        if bool(albumIdMap) == False:
            albumIdMap = loadListOfAlbumsFromCache(googleService, True)

        if bool(albumIdMap) == False:
            print(f"No album Id to process photos of")
            
        return albumIdMap

api.add_resource(AuthorizeWithGoogle, '/auth')
api.add_resource(PhotoAlbums, '/albums')
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run()