import os
from gphotospy.media import MediaItem
from loguru import logger
from database.sql_engine import SqlConnection
from database.sql_engine import SqlEngine
from database.models.photos import Photo
from modules.image_downloader import ImageDownloader
from modules.image_hash import ImageModule


class GoogleImages(object):
    # def getPhotoFromDb(photoId: str, connection: SqlConnection):
    #     with SqlEngine(connection) as engine:
    #         photoFromDb: Photo
    #         photoFromDb = engine.select(Photo).filter(
    #             Photo.id == photoId).first()

    #         return photoFromDb

    def getPhotosFromDb(photoIds, connection: SqlConnection):
        with SqlEngine(connection) as engine:
            return engine.select(Photo) \
                .filter(Photo.id.in_(photoIds)) \
                .all()

    def storePhotosInDb(photos, connection: SqlConnection):
        with SqlEngine(connection) as engine:
            for photo in photos:
                engine.add(photo)

    def createPhoto(albumId: str, userId: str, image: MediaItem, CONFIG):
        try:
            imageDownloadName = GoogleImages.getImageName(image)
            ImageDownloader.downloadPhoto(image, imageDownloadName, CONFIG.IMAGE_DOWNLOAD_FOLDER)
            imageHash = GoogleImages.getImageHash(image, imageDownloadName, CONFIG)
            photo = GoogleImages.getPhotoToStore(image, albumId, userId, imageHash)
            # logger.debug(photo.toString())

            return photo
        except Exception as e:
            logger.exception(e)
            
        return None

    def getImageHash(image: MediaItem, imageDownloadName, CONFIG) -> ImageModule:
        image_path = os.path.join(CONFIG.IMAGE_DOWNLOAD_FOLDER, imageDownloadName)

        with ImageModule(image_path, CONFIG) as imageHash:
            logger.debug(f"hash of the image {imageHash.hash}"
                        + f"Hash string {imageHash.hashString} "
                        + f"has length {len(imageHash.hashString)}")
            logger.debug(f"Hash in chunks format: "
                        + f"{imageHash.hashChuncks()}")

            return imageHash

    def getPhotoToStore(image: MediaItem, albumId: str, userId: str, imageHash: ImageModule):

        photo = Photo()
        photo.albumId = albumId
        hashChunks = imageHash.hashChuncks()
        photo.baseUrl = image.get_url()        
        photo.filename = image.filename()
        photo.hash_chunk1 = hashChunks[0]
        photo.hash_chunk2 = hashChunks[1]
        photo.hash_chunk3 = hashChunks[2]
        photo.hash_chunk4 = hashChunks[3]
        photo.hash_chunk5 = hashChunks[4]
        photo.hash_chunk6= hashChunks[5]
        photo.hash_chunk7 = hashChunks[6]
        photo.hash_chunk8 = hashChunks[7]
        
        photo.id = image.val.get("id")
        photo.have_found_similar_images = False
        photo.userId = userId

        return photo

    def cleanImageIfOnLocal(image: MediaItem, CONFIG):
        try:
            downloadedImageName = GoogleImages.getImageName(image)
            ImageDownloader.deleteImage(downloadedImageName, CONFIG.IMAGE_DOWNLOAD_FOLDER)
        except Exception as e:
            logger.error(e)
    
    def getImageName(photo:MediaItem):
        photoId = photo.val.get("id")
        photoExtension = photo.filename().split('.')[1]
        return f"{photoId}.{photoExtension}"