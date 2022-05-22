import json 

from gphotospy.album import *
from gphotospy.media import *

from flask import Blueprint, redirect, request, url_for
from flask_app.blueprints.albums.models.albums import PhotoAlbum
from flask_app.blueprints.albums.models.photos import Photos
from flask_app.sqldb.appdb import db

from flask_app.blueprints.google_photos_service import gphoto_service
from flask_app.blueprints.user.models.user_auth_model import UserOauth
from flask_app.blueprints.user.user_authentication import login_is_required
from flask_app.applogger import logger

bp = Blueprint('photo_albums', __name__, url_prefix='/photo_albums')

@bp.route("/")
@login_is_required
def getUserAlbums(user):

    albums = [album.serialize for album in getAllAlbumsOfUser(user)]
    return json.dumps(albums)

@bp.route("/reload")
@login_is_required
def reloadUserAlbums(user):
    googleService = gphoto_service.getGooglePhotoService(user)
    
    logger.info("reloading albums")
    if googleService == None:
        logger.error("failed to create google service for user {}", user)
        return "failed to create google service", 500
    
    for album in gphoto_service.getAlbumsOfUserFromGoogle(googleService):
        logger.debug(f"Loading albumid: {album['id']}  title:{album['title']}")
        if PhotoAlbum.getAlbum(album["id"]) == None:
            db.session.add(PhotoAlbum.createAlbumObject(user.id, album))

    db.session.commit()

    return "Albums have been reloaded" #redirect(url_for("photo_albums.getUserAlbums"))

@bp.route("/view/<album_title>")
@login_is_required
def viewAlbum(user, path_arguments):
    album_title = path_arguments["album_title"]
    logger.debug(f"album_title: {album_title}")
    
    if album_title == None or album_title == "":
        return "Unable to read album_title from request"

    logger.info(f"Getting album of title: {album_title}")
    albums = [album.serialize for album in PhotoAlbum.getAlbumsWithTitle(user.id, album_title)]

    return json.dumps(albums)


@bp.route("/view/<album_title>/photos")
@login_is_required
def viewAlbumPhotos(user, path_arguments):
    album_title = path_arguments["album_title"]
    logger.debug(f"album_title: {album_title}")
    
    if album_title == None or album_title == "":
        return "Unable to read album_title from request"

    logger.info(f"Getting album of title: {album_title}")
    albumIds = [album.id for album in PhotoAlbum.getAlbumsWithTitle(user.id, album_title)]
    photos = []
    for albumId in albumIds:
        photos += Photos.getPhotosOfAlbum(albumId) 
    photos = [photo.serialize for photo in photos]

    return json.dumps(photos)

def getAllAlbumsOfUser(user: UserOauth):
    return PhotoAlbum.getAlbumsOfUser(user.id)


def post(self):
    # json_data = request.get_json(force=True)

    if request.form is None \
        or len(request.form) == 0 \
        or "albumId" not in request.form:

        return redirect(self.api.url_for("photo_albums"))


    print(request.form["albumId"])

    return redirect(self.api.url_for("photo_albums"))