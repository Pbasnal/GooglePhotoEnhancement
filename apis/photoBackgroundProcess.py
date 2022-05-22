import json
import numpy as np
from cacheservice import DictCache
from apis.AuthorizeWithGoogle import getGooglePhotoService
from gphotospy.media import *
from PhotoData import PhotoData
from imagehash import ImageHash
import imagehash
from PIL import Image
from GoogleMediaItem import GoogleMediaItem
from apis.messagebus import PHOTO_QUEUE

PHOTO_TASK_FILE = "photoTask.json"
DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"

def registerMessageListener(channel):
    channel.basic_consume(queue=PHOTO_QUEUE, on_message_callback=processPhotosOfAlbum, auto_ack=True)

def processPhotosOfAlbum(consumer, eventMethod, eventProperties, serialisedMessage):
    print(f"Recieved {serialisedMessage}")
    googleService = getGooglePhotoService(userId)
    mediaManager = Media(googleService)

    userId, albumId, photo = getInputsFromMessage(serialisedMessage)
    photo = GoogleMediaItem(mediaManager.get(photo["id"]))
    

    with DictCache("similarPhoto.json", "json") as similarPhotoCache:
        similarPhotos = similarPhotoCache.getForKey(photo.id())
        if similarPhotos != None:
            return

    idsOfSimilarPhotos = []
    with DictCache("photoCache.json") as photoCache:
        photoData = photoCache.getForKey(photo.id())
        if photoData.hash == None:
            hash = getPhotoHash(photo, mediaManager)
            photoData.hash = hashToString(hash)
            photoCache.save(photo.id(), photo)
        else:
            hash = stringToHash(photo.photoHash())

        if hash == None:
            return

        print(f"processing similar photos for photoId: {photo.id()}")
        idsOfSimilarPhotos = getIdsOfSimilarPhotos(photo, photoCache, hash)        
        if idsOfSimilarPhotos == None or len(idsOfSimilarPhotos) == 0:
            return

    print(f"Found {len(idsOfSimilarPhotos)} similar photos to photoId {photo.id()}")
    with DictCache("similarPhoto.json", "json") as similarPhotoCache:
        similarPhotoCache.save(photo.id(), idsOfSimilarPhotos)

def getIdsOfSimilarPhotos(photo, photoCache, hash):
    idsOfSimilarPhotos = []
    for similarPhotoId, similarPhoto in photoCache.get():
        if similarPhotoId == photo.id() or similarPhoto.photoHash() == None:
            continue

        similarPhotoHash = stringToHash(similarPhoto.photoHash())
        diff = similarPhotoHash - hash
        diffPercentage = (10 - diff) / 10 * 100
        if diffPercentage < 60:
            continue
        idsOfSimilarPhotos.append(similarPhotoId)
    return idsOfSimilarPhotos

def getPhotoHash(photo, mediaManager):
    if "hash" in photo and photo["hash"] != None:
        return stringToHash(photo["hash"])

    base_photo = GoogleMediaItem(mediaManager.get(photo["id"]))
    raw_photo = downloadPhoto(base_photo)
    hash = imagehash.average_hash(raw_photo)
    raw_photo.close()
    if hash == None:
        return None
    return hash

def getInputsFromMessage(serialisedMessage):
    message = json.loads(serialisedMessage)
    userId = message["userId"]
    albumId = message["albumId"]
    photo = message["photo"]
    return userId, albumId, photo


def hashToString(imgHash):
    return ''.join(str(b) for b in 1 * imgHash.hash.flatten())


def stringToHash(stringHash):
    width = int(np.ceil(len(stringHash)/4))
    strhash = '{:0>{width}x}'.format(int(stringHash, 2), width=width)

    str_to_int = int(strhash, 16)
    int_to_binary = np.array([bool(int(b))
                             for b in "{0:0>64b}".format(str_to_int)])
    arr_to_hash = int_to_binary.reshape((8, 8))

    return ImageHash(arr_to_hash)


def downloadPhoto(photo):
    photo_filename = photo["filename"]
    download_path = os.path.join(DOWNLOAD_FOLDER, photo_filename)

    if not os.path.exists(download_path):
        with open(download_path, 'wb') as output:
            output.write(photo.raw_download())

    return getImage(download_path)


def getImage(photo_path):
    if os.path.exists(photo_path) == False:
        return None
    return Image.open(photo_path)
