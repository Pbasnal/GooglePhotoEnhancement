import google
import random

from gphotospy.album import *
from gphotospy.media import *
from flask_app.blueprints.user import config
from flask_app.applogger import logger

from googleapiclient.discovery import build


def getGooglePhotoService(user):

    service_object = {
        "secrets": config.CLIENT_SECRET_FILE
    }
    credentials = credentials_from_user(user)
    try:
        service = build(config.API_SERVICE_NAME, config.API_VERSION,
                        static_discovery=False, credentials=credentials)
        service_object["service"] = service
        return service_object
    except Exception as e:
        logger.error("Failed to create google photo service {}", e)
    return None


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


def getAlbumsOfUserFromGoogle(googleService):
    album_manager = Album(googleService)
    album_iterator = album_manager.list()

    for album in album_iterator:
        album_title = album.get('title')
        album["title"] = album_title if album_title != None else "Untitled"
        yield album


def getPhotosOfUserFromGoogle(googleService, photoIds):
    mediaManager = Media(googleService)
    # n = random. random()

    photos = []
    for photoId in photoIds:
        base_photo = mediaManager.get(photoId)
        photos.append(MediaItem(base_photo))

        # logger.debug(f"{n} -> {base_photo}")

    return photos
