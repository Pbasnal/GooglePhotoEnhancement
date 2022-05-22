import json
import typing
import uuid

from loguru import logger
from flask_app.blueprints.albums.models.photos import Photos
from flask_app.blueprints.similar_images.models.similar_images import SimilarImages
from flask_app.blueprints.user.models.user_auth_model import UserOauth
from flask_app.blueprints.google_photos_service import gphoto_service

from flask_app.sqldb.appdb import db
from flask import Blueprint, jsonify, render_template
from flask_app.blueprints.albums.models.albums import PhotoAlbum
from flask_app.blueprints.similar_images.models.process_tracker import ProcessTracker

from flask_app.blueprints.user.user_authentication import login_is_required

bp = Blueprint('similar_images', __name__, url_prefix='/similar_images')


class RenderableSimilarImages(object):
    def __init__(self):
        self.imageId: str
        self.imageUrl: str
        self.similarityScore: float

    def serialize(self):
        return {
            "imageId": self.imageId,
            "imageUrl": self.imageUrl,
            "similarityScore": self.similarityScore
        }


class RenderableParentImage(object):
    def __init__(self):
        self.imageId:  str
        self.imageUrl: str
        self.similarImages = dict()

    def addSimilarImage(self, image, similarityScore):
        if image.id in self.similarImages.keys():
            return
        similarImage = RenderableSimilarImages()
        similarImage.imageId = image.id
        similarImage.imageUrl = image.baseUrl
        similarImage.similarityScore = similarityScore

        self.similarImages[image.id] = similarImage

    def serialize(self):
        return {
            "imageId": self.imageId,
            "imageUrl": self.imageUrl,
            "similarImages": [image.serialize() for image in self.similarImages.values()]
        }


class SimilarImageCollection(object):

    def __init__(self):
        self.imageCollection = dict()
        self.imageIdSet = set()

    def add(self, imageId, image):
        if imageId in self.imageIdSet:
            return

        parentImage = RenderableParentImage()
        parentImage.imageId = imageId
        parentImage.imageUrl = image.baseUrl
        self.imageCollection[imageId] = parentImage
        self.imageIdSet.add(imageId)

    def addSimilarImage(self, image, similarImage, similarityScore):
        if image.id not in self.imageIdSet:
            return
        if image.id == similarImage.id:
            return
        self.imageCollection[image.id].addSimilarImage(
            similarImage, similarityScore)

    def serialize(self):
        return [image.serialize()
                for image in self.imageCollection.values()
                if len(image.similarImages) > 0]


@bp.route("/<int:page>")
@login_is_required
def get_all_similar_images(user: UserOauth, path_arguments):
    page = path_arguments["page"] if "page" in path_arguments else 1
    page = int(page)
    logger.debug("similar image list")

    allSimilarImages = getSimilarImages(user.id, page, perPage=10)
    photos = getPhotosForSimilarImages(user, allSimilarImages)
    
    photosMap = {photo.id: photo for photo in photos}

    for photoId in photosMap.keys():
        logger.debug(f"id:{photoId}, photo:{photosMap[photoId].serialize}")

    similarImageCollection = buildSimilarImageCollection(allSimilarImages, photosMap)

    logger.debug(similarImageCollection.serialize())
    return render_template("index.html", similarImagesMap=similarImageCollection.serialize())
    # return jsonify(similarImageCollection.serialize())

def buildSimilarImageCollection(allSimilarImages, photosMap):
    imageHashSet = set()
    similarImageCollection = SimilarImageCollection()
    similarImage: SimilarImages
    for similarImage in allSimilarImages:
        # logger.debug(similarImage.serialize)

        keyImageId: str()
        similarImageId = str()
        if similarImage.imageId not in imageHashSet \
                and similarImage.similarImageId not in imageHashSet:
            imageHashSet.add(similarImage.imageId)
            keyImageId = similarImage.imageId
            similarImageId = similarImage.similarImageId

        elif similarImage.imageId in imageHashSet:
            keyImageId = similarImage.imageId
            similarImageId = similarImage.similarImageId
        elif similarImage.similarImageId in imageHashSet:
            keyImageId = similarImage.similarImageId
            similarImageId = similarImage.imageId

        similarImageCollection.add(keyImageId, photosMap[keyImageId])
        similarImageCollection.addSimilarImage(photosMap[keyImageId],
                                               photosMap[similarImageId],
                                               similarImage.similarityScore)
        # break
    return similarImageCollection

def getSimilarImages(userId, page, perPage):
    similarImages = SimilarImages.getImagesSimilarForUser(
        userId, page, perPage)
    imageIdSet = set()
    [(imageIdSet.add(image.imageId), imageIdSet.add(image.similarImageId))
     for image in similarImages]
    
    allSimilarImages = []
    for imageId in imageIdSet:
        allSimilarImages += SimilarImages.getImagesSimilarTo(imageId)

    return allSimilarImages

def getPhotosForSimilarImages(user, similarImages):
    imageIdSet = set()
    [(imageIdSet.add(image.imageId), imageIdSet.add(image.similarImageId))
     for image in similarImages]
    
    photos = []
    googleService = gphoto_service.getGooglePhotoService(user)
    for googlePhoto in gphoto_service.getPhotosOfUserFromGoogle(googleService, imageIdSet):
        photo = Photos()
        photo.baseUrl = googlePhoto.get_url()        
        photo.filename = googlePhoto.filename()

        photo.id = googlePhoto.val.get("id")
        photo.have_found_similar_images = False
        photo.userId = user.id

        photos.append(photo)
    return photos




@bp.route("/start")
@login_is_required
def similar_images(user):
    albums = PhotoAlbum.getAlbumsOfUser(user.id)
    albums = {album.id: album for album in albums}

    albums_in_process = ProcessTracker.getProcessesOfUser(user.id)
    albums_in_process = {album.albumId: album for album in albums_in_process}

    for albumid in albums.keys():
        if albumid in albums_in_process.keys():
            continue
        album_process = ProcessTracker()
        album_process.id = str(uuid.uuid4())
        album_process.albumId = albumid
        album_process.similarImagesStatus = "NotStarted"
        album_process.userId = albums[albumid].userId

        db.session.add(album_process)
    db.session.commit()

    return "similar images"


@bp.route("/<imageid>")
@login_is_required
def get_similar_images(user, path_arguments):
    logger.debug("similar image list")
    logger.debug(path_arguments)

    imageid = path_arguments["imageid"]
    similarImages = SimilarImages.getImagesSimilarTo(imageid)

    if similarImages is None or len(similarImages) == 0:
        return "No images", 404

    similarImages = [si.to_json() for si in similarImages]

    return json.dumps(similarImages), 200


class SimilarImageStats:
    count_of_albums = 0
    count_of_albums_which_have_process_attached = 0

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


@bp.route("/stats")
@login_is_required
def similar_images_stats(user):
    albums = PhotoAlbum.getAlbumsOfUser(user.id)
    albums_currently_getting_processed = ProcessTracker.getProcessesOfUser(
        user.id)

    similar_images_stats = SimilarImageStats()
    similar_images_stats.count_of_albums = len(albums)
    similar_images_stats.count_of_albums_which_have_process_attached = \
        len(albums_currently_getting_processed)

    return similar_images_stats.to_json()
