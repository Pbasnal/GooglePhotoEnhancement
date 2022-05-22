import time
from loguru import logger
from google_service.google_photo_service import GooglePhotoService
from modules.photo_albums import getNotStartedAlbums, markProcessAsCompleteForAlbum
from configs.config import Config
from database.models.photos import Photo
from database.models.process_tracker import ProcessTracker
from database.sql_engine import SqlConnection
from modules.google_images import GoogleImages
from gphotospy.media import MediaItem


class ImageDownloaderJob(object):

    def run(self, connection: SqlConnection,  gservice: GooglePhotoService, CONFIG: Config):
        while(True):
            self.downloadImages(connection, gservice, CONFIG)
            time.sleep(3)

    def getAlbumPhotoMapToProcess(self, connection, gservice, CONFIG):
        albumPhotosZip = dict()
        for processTrackers in getNotStartedAlbums(CONFIG.BATCH_SIZE_FOR_ALBUM_PROCESS, connection):
            logger.debug(
                f"ImageDownloader: Got an album batch to download images. Batch size {len(processTrackers)}")
            album: ProcessTracker
            for album in processTrackers:
                if album.albumId != "AJ36JaQJtcU8597xCPM_dNY-9J-D_MJiAooc4iEpGK2L60A_m5FPlgDjfrinUqNQYCBj61FUiqm1":
                    continue
                logger.debug(album.toString())
                googlePhoto: MediaItem
                gservice = gservice.getGoogleServiceForUser(album.userId)
                for googlePhoto in gservice.photosOfAlbum(album.albumId):
                    if album.albumId not in albumPhotosZip.keys():
                        albumPhotosZip[album.albumId] = []
                    albumPhotosZip[album.albumId].append(
                        (album.userId, googlePhoto))
                # Just for local testing.
                break

        if len(albumPhotosZip) == 0:
            logger.debug(f"ImageDownloader: No more albums to process")
            return None

        return albumPhotosZip

    def getChunksOfArray(array, chunkSize):
        return [array[i: i + chunkSize]
                for i in range(0, len(array), chunkSize)]

    def getPhotosToInsertIntoDb(self, albumId, albumPhotos, connection, CONFIG):
        photoIds = [photo.val.get("id") for _, photo in albumPhotos]
        existingPhotoIds = [existingPhoto.id
                            for existingPhoto in GoogleImages.getPhotosFromDb(photoIds, connection)]

        # Clean existing photos from local if they were downloaded previously
        # [GoogleImages.cleanImageIfOnLocal(photo, CONFIG)
        #  for _, photo in albumPhotos if photo.val.get("id") in existingPhotoIds]

        photosToInsertInDb = [GoogleImages.createPhoto(albumId, userId, photo, CONFIG)
                              for userId, photo in albumPhotos if photo.val.get("id") not in existingPhotoIds]

        return photosToInsertInDb

    def downloadImages(self, connection: SqlConnection, gservice: GooglePhotoService, CONFIG: Config):
        chunksize = 1000

        logger.debug(
            f"ImageDownloader: processing for batch size: {CONFIG.BATCH_SIZE_FOR_ALBUM_PROCESS}")
        logger.debug(
            f"ImageDownloader: processing for batch size: {CONFIG.BATCH_SIZE_FOR_ALBUM_PROCESS}")

        albumPhotosMap = self.getAlbumPhotoMapToProcess(connection, gservice, CONFIG)

        if albumPhotosMap == None:
            return

        for albumId in albumPhotosMap.keys():
            albumPhotos = albumPhotosMap[albumId]

            photosToInsertInDb = self.getPhotosToInsertIntoDb(
                albumId, albumPhotos, connection, CONFIG)
            photoChunks = ImageDownloaderJob.getChunksOfArray(
                photosToInsertInDb, chunksize)

            for photosChunk in photoChunks:
                logger.info(
                    f"ImageDownloader: Storing {len(photosChunk)} photos in db")
                GoogleImages.storePhotosInDb(photosChunk, connection)

            logger.debug(
                f"ImageDownloader: updating process tracker status {albumId}")
            markProcessAsCompleteForAlbum(albumId, connection)
