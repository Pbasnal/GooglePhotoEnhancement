import os
from gphotospy.media import MediaItem
from loguru import logger

class ImageDownloader(object):
    def downloadPhoto(photo: MediaItem, imageDownloadName, download_folder):
        download_path = os.path.join(download_folder, imageDownloadName)

        try:
            if not os.path.exists(download_path):
                with open(download_path, 'wb') as output:
                    output.write(photo.raw_download())
            else:
                logger.info(f"File {imageDownloadName} already exists, skipping download")
        except Exception as e:
            logger.exception(e)
            logger.error(os.path.abspath(os.getcwd()))

    def deleteImage(imageDownloadName, download_folder):
        download_path = os.path.join(download_folder, imageDownloadName)

        logger.debug(f"deleting image at {download_path}")
        try:
            if os.path.exists(download_path):
                os.remove(download_path)
        except Exception as e:
            logger.exception(e)

        
        