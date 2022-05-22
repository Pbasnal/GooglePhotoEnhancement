from loguru import logger
from database.sql_engine import SqlEngine
from similar_image_job import SimilarImageJob
from google_service.google_photo_service import GooglePhotoService
from modules.photo_albums import getNotStartedAlbums
from configs.config import Config
from database.models.photos import Photo
from database.models.process_tracker import ProcessTracker
from database.sql_engine import SqlConnection
from modules.google_images import GoogleImages
from gphotospy.media import MediaItem

class PhotoTestJob(object):

    def run(self, connection:SqlConnection,  gservice:GooglePhotoService, CONFIG:Config):
        similarImageJob = SimilarImageJob()
        with SqlEngine(connection) as engine:
            notProcessedPhotos = engine.select(Photo) \
                    .filter(Photo.filename.is_("DSC_0719.JPG")) \
                    .all()
            albumId = notProcessedPhotos[0].albumId
            allPhotosOfAlbum = engine.select(Photo) \
                    .filter(Photo.albumId.is_(albumId)) \
                    .all()

            for photo in allPhotosOfAlbum:
                logger.debug(photo.toString())

        similarImageJob.getImagesSimilarToPhotos(notProcessedPhotos, connection)