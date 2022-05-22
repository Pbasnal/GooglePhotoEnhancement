import time
import typing
import uuid
import imagehash
import numpy as np
import logging

from imagehash import ImageHash
from loguru import logger
from sqlalchemy import or_
from database.models.similar_images import SimilarImages
from database.sql_engine import SqlEngine
from configs.config import Config
from database.models.photos import Photo
from database.sql_engine import SqlConnection


class SimilarImageJob(object):

    def run(self, connection: SqlConnection, CONFIG: Config):

        # logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
        while(True):
            self.findSimilarImages(connection, CONFIG)
            time.sleep(3)

    def findSimilarImages(self, connection: SqlConnection, CONFIG: Config):

        batch_size = CONFIG.BATCH_SIZE_FOR_SIMILAR_PHOTO_PROCESS
        with SqlEngine(connection) as engine:
            notProcessedPhotos = engine.select(Photo) \
                .filter(Photo.have_found_similar_images.is_(False)) \
                .limit(batch_size) \
                .all()

        logger.debug(
            f"similarImages: photos not processed yet: {len(notProcessedPhotos)}")
        similarImagesMap = self.getImagesSimilarToPhotos(
            notProcessedPhotos, connection)

        with SqlEngine(connection) as engine:
            processedPhotoIds = [photo.id for photo in notProcessedPhotos]
            processedPhotos = engine.select(Photo) \
                .filter(Photo.id.in_(processedPhotoIds)) \
                .all()

            photo: Photo
            for photo in processedPhotos:
                photo.have_found_similar_images = True

            for imageId in similarImagesMap.keys():
                for similarImage in similarImagesMap[imageId]:
                    existing = engine.select(SimilarImages) \
                        .filter(SimilarImages.imageId == imageId
                                and SimilarImages.similarImageId == similarImage.similarImageId) \
                        .all()
                    if existing is not None and len(existing) > 0:
                        continue

                    engine.add(similarImage)

    def getImagesSimilarToPhotos(self, notProcessedPhotos, connection):

        notProcessedPhoto: Photo
        similarImagesMap = dict()
        with SqlEngine(connection) as engine:
            for notProcessedPhoto in notProcessedPhotos:
                similarPhotos = self.getSimilarImagesFromDb(
                    notProcessedPhoto, engine)
                logger.debug(f"similarImages: Images similar to \
                {notProcessedPhoto.id} are {len(similarPhotos)} ")

                if len(similarPhotos) == 0:
                    continue

                # similarImages = list(
                #     filter(lambda x: x.id != notProcessedPhoto.id, similarImages2))

                similarImagesMap[notProcessedPhoto.id] = []

                logger.info("Processing image")
                imageHashOfRequestedImage = self.getHashOfPhoto(
                    notProcessedPhoto)
                similarImagesMap[notProcessedPhoto.id] = []
                for photo in similarPhotos:
                    similarImageModel = self.getSimilarImageModel(notProcessedPhoto, imageHashOfRequestedImage, photo)
                    if similarImageModel is None:
                        continue
                    similarImagesMap[notProcessedPhoto.id].append(similarImageModel)

        return similarImagesMap

    def getSimilarImagesFromDb(self, photo, engine) -> typing.List[Photo]:

        photos = engine.select(Photo) \
            .filter(Photo.hash_chunk1.is_(photo.hash_chunk1),
                    or_(Photo.hash_chunk2.is_(photo.hash_chunk2),
                        Photo.hash_chunk3.is_(photo.hash_chunk3),
                        Photo.hash_chunk4.is_(photo.hash_chunk4),
                        Photo.hash_chunk5.is_(photo.hash_chunk5),
                        Photo.hash_chunk6.is_(photo.hash_chunk6),
                        Photo.hash_chunk7.is_(photo.hash_chunk7),
                        Photo.hash_chunk8.is_(photo.hash_chunk8))) \
            .all()

        photos = photos + engine.select(Photo) \
            .filter(Photo.hash_chunk2.is_(photo.hash_chunk2),
                    or_(Photo.hash_chunk3.is_(photo.hash_chunk3),
                        Photo.hash_chunk4.is_(photo.hash_chunk4),
                        Photo.hash_chunk5.is_(photo.hash_chunk5),
                        Photo.hash_chunk6.is_(photo.hash_chunk6),
                        Photo.hash_chunk7.is_(photo.hash_chunk7),
                        Photo.hash_chunk8.is_(photo.hash_chunk8))) \
            .all()

        photos = photos + engine.select(Photo) \
            .filter(Photo.hash_chunk3.is_(photo.hash_chunk3),
                    or_(Photo.hash_chunk4.is_(photo.hash_chunk4),
                        Photo.hash_chunk5.is_(photo.hash_chunk5),
                        Photo.hash_chunk6.is_(photo.hash_chunk6),
                        Photo.hash_chunk7.is_(photo.hash_chunk7),
                        Photo.hash_chunk8.is_(photo.hash_chunk8))) \
            .all()

        photos = photos + engine.select(Photo) \
            .filter(Photo.hash_chunk4.is_(photo.hash_chunk4),
                    or_(Photo.hash_chunk5.is_(photo.hash_chunk5),
                        Photo.hash_chunk6.is_(photo.hash_chunk6),
                        Photo.hash_chunk7.is_(photo.hash_chunk7),
                        Photo.hash_chunk8.is_(photo.hash_chunk8))) \
            .all()

        photos = photos + engine.select(Photo) \
            .filter(Photo.hash_chunk5.is_(photo.hash_chunk5),
                    or_(Photo.hash_chunk6.is_(photo.hash_chunk6),
                        Photo.hash_chunk7.is_(photo.hash_chunk7),
                        Photo.hash_chunk8.is_(photo.hash_chunk8))) \
            .all()

        photos = photos + engine.select(Photo) \
            .filter(Photo.hash_chunk6.is_(photo.hash_chunk6),
                    or_(Photo.hash_chunk7.is_(photo.hash_chunk7),
                        Photo.hash_chunk8.is_(photo.hash_chunk8))) \
            .all()

        photos = photos + engine.select(Photo) \
            .filter(Photo.hash_chunk7.is_(photo.hash_chunk7),
                    Photo.hash_chunk8.is_(photo.hash_chunk8)) \
            .all()

        photos = list(
            filter(lambda x: x.id != photo.id, photos))

        return photos

    def getHashOfPhoto(self, photo: Photo) -> imagehash:

        hash = photo.hash_chunk1 + photo.hash_chunk2 + \
            photo.hash_chunk3 + photo.hash_chunk4 + \
            photo.hash_chunk5 + photo.hash_chunk6 + \
            photo.hash_chunk7 + photo.hash_chunk8
        hash = self.stringToHash(hash)

        logger.info(f"{photo.id} imagehash: {hash}")

        return hash

    def stringToHash(self, stringHash):
        width = int(np.ceil(len(stringHash)/4))
        strhash = '{:0>{width}x}'.format(int(stringHash, 2), width=width)

        str_to_int = int(strhash, 16)
        int_to_binary = np.array([bool(int(b))
                                  for b in "{0:0>64b}".format(str_to_int)])
        arr_to_hash = int_to_binary.reshape((8, 8))

        return ImageHash(arr_to_hash)

    def getSimilarImageModel(self, originalImage: Photo, originalImageHash, imageToCompareWith: Photo):

        similarImageHash = self.getHashOfPhoto(imageToCompareWith)
        diff = originalImageHash - similarImageHash

        diffPercentage = (64 - diff) / 64 * 100

        similarPhotoModel = SimilarImages()
        similarPhotoModel.id = str(uuid.uuid4())
        similarPhotoModel.userId = originalImage.userId
        similarPhotoModel.imageId = originalImage.id
        similarPhotoModel.similarImageId = imageToCompareWith.id
        similarPhotoModel.similarityScore = diffPercentage

        if similarPhotoModel.similarityScore < 75:
            return None

        logger.debug(
            f"{originalImage.filename} - {imageToCompareWith.filename} : {diff} {diffPercentage}%")
        return similarPhotoModel
