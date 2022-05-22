# import json
from multiprocessing.dummy import Process
import uuid

from loguru import logger
from sqlalchemy import func
from flask_app.blueprints.albums.models.photos import Photos
from flask_app.blueprints.similar_images.models.similar_images import SimilarImages
from flask_app.blueprints.user.models.user_auth_model import UserOauth


from flask_app.sqldb.appdb import db
from flask import Blueprint, jsonify
from flask_app.blueprints.albums.models.albums import PhotoAlbum
from flask_app.blueprints.similar_images.models.process_tracker import ProcessTracker

from flask_app.blueprints.user.user_authentication import login_is_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route("/")
@login_is_required
def getCurrentStatus(user: UserOauth):

    status = dict()

    status["album"] = getAlbumMeta(user)
    status["photos"] = getPhotoMeta(user)
    status["processTracker"] = getProcessTrackersMeta(user)
    status["similarImages"] = getSimilarImagesMeta(user)

    return jsonify(status)

def getSimilarImagesMeta(user: UserOauth):
    similarImagesMeta = dict()

    numberOfSimilarImages = SimilarImages.query.filter(SimilarImages.userId == user.id) \
        .count()
    similarImagesMeta["numberOfSimilarImages"] = numberOfSimilarImages
        
    return similarImagesMeta


def getProcessTrackersMeta(user: UserOauth):
    processTrackerMeta = []

    processTrackers = ProcessTracker.query.filter(ProcessTracker.userId == user.id) \
        .with_entities(ProcessTracker.similarImagesStatus,
                       func.count('*'))\
        .group_by(ProcessTracker.similarImagesStatus) \
        .all()
    
    for row in processTrackers:
        processMeta = {
            "similarImageStatusOoAlbum": row[0],
            "count": row[1]
        }
        processTrackerMeta.append(processMeta)
        
    return processTrackerMeta


def getPhotoMeta(user: UserOauth):
    photoMeta = dict()
    photoMeta["totalNumberOfPhotosOfUser"] = Photos.query.filter(Photos.userId == user.id) \
        .count()

    photosGroupedByAlbum = Photos.query\
        .with_entities(Photos.albumId,
                       Photos.have_found_similar_images,
                       func.count('*'))\
        .filter(Photos.userId == user.id) \
        .group_by(Photos.albumId, Photos.have_found_similar_images) \
        .all()
    photoMeta["photosGroupedByAlbum"] = []
    for row in photosGroupedByAlbum:
        photoAlbumMeta = {
            "albumId": row[0],
            "haveFoundSimilarImages": row[1],
            "count": row[2]
        }
        photoMeta["photosGroupedByAlbum"].append(photoAlbumMeta)

    return photoMeta


def getAlbumMeta(user: UserOauth):
    albumCount = PhotoAlbum.query \
        .filter(PhotoAlbum.userId == user.id) \
        .count()

    albumData = dict()
    albumData["count"] = albumCount

    albumData["albums"] = [[album[0], album[1]] for album in PhotoAlbum.query
                           .filter(PhotoAlbum.userId == user.id)
                           .with_entities(PhotoAlbum.id, PhotoAlbum.title)
                           .all()]

    return albumData
