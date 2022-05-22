from imagehash import ImageHash
import numpy as np

import threading
from modules.image_hash import ImageModule
from photo_test_job import PhotoTestJob
from similar_image_job import SimilarImageJob
from image_downloader_job import ImageDownloaderJob
from database.sql_engine import SqlConnection
from configs.config_loader import loadConfigs
from loguru import logger
from google_service.google_photo_service import GooglePhotoService

def stringToHash(stringHash):
    width = int(np.ceil(len(stringHash)/4))
    strhash = '{:0>{width}x}'.format(int(stringHash, 2), width=width)

    str_to_int = int(strhash, 16)
    int_to_binary = np.array([bool(int(b))
                                for b in "{0:0>64b}".format(str_to_int)])
    arr_to_hash = int_to_binary.reshape((8, 8))

    return ImageHash(arr_to_hash)

def testImageHashDiff(CONFIG):
    imageFolder = "../flask_app/frontend/static/img/"
    img1name = "AJ36JaTTJiLpHBl-Dv1JPk-2xHvYGMyZVAeiqUWcgLfLw1jFthNKhUv6F35FJjNtCayqgkoXRu0oskmZsa1Vzc7TwjymWRh1AA.jpg"
    img2name = "AJ36JaROeqibzBTguCt0JBcBPyu6zqhjMtTwEDfu1mhC4qv-rPMrDFR8QKAGOH4guD3q8AinUkeYzC6mGj8gRHMtFS15mvAjIg.jpg"
    with ImageModule(f"{imageFolder}{img1name}", CONFIG) as img1:
        with ImageModule(f"{imageFolder}{img2name}", CONFIG) as img2:
            logger.debug(img1.hash - img2.hash)
    # im1 = stringToHash("1111111111111111111110010100100100001111000000110000000000000000")
    # im2 = stringToHash("1111111111100111111011111100001101000010000000000000000000010000")
    # diff = im1 - im2
    # logger.debug(64 - diff)


if __name__ == "__main__":
    CONFIG = loadConfigs()
    # testImageHashDiff(CONFIG)
    logger.add("background_jobs.log", rotation="5 MB", compression="zip")


    gservice = GooglePhotoService()

    imageDownloaderJob = ImageDownloaderJob()

    similarImageJob = SimilarImageJob()

    photoTestJob = PhotoTestJob()

    logger.info(f"Configs {CONFIG.__dict__}")
    with SqlConnection(CONFIG.SQLALCHEMY_DATABASE_URI) as connection:
        # photoTestJob.run(connection, gservice, CONFIG)

        # processThread = threading.Thread(target=imageDownloaderJob.run, args=(connection, gservice, CONFIG))
        # processThread.start()

        processThread = threading.Thread(target=similarImageJob.run, args=(connection, CONFIG))
        processThread.start()
        

        