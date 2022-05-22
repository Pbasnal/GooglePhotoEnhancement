import json
import numpy as np
from cacheservice import DictCache
from apis.AuthorizeWithGoogle import getGooglePhotoService
from gphotospy.media import *
from imagehash import ImageHash
import imagehash
from PIL import Image
from GoogleMediaItem import GoogleMediaItem
from apis.messagebus import PHOTO_QUEUE

PHOTO_TASK_FILE = "photoTask.json"
DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"

def registerMessageListener(channel):
    print(f"Registering listener processPhotosOfAlbum")
    channel.basic_consume(queue=PHOTO_QUEUE, on_message_callback=processPhotosOfAlbum, auto_ack=True)

def processPhotosOfAlbum(ch, method, properties, serialisedMessage):
    print(f"Recieved {serialisedMessage}")

    userId, albumId, photo = getInputsFromMessage(serialisedMessage)

    googleService = getGooglePhotoService(userId)
    mediaManager = Media(googleService)
    photo = GoogleMediaItem(mediaManager.get(photo["id"]))

    idsOfSimilarPhotos = []
    with DictCache("photoCache.json") as photoCache:
        photoData = photoCache.getForKey(photo.id())
        if photoData.hash == None:
            hash = getPhotoHash(photoData, mediaManager)
            photoData.hash = hashToString(hash)
            photoCache.save(photo.id(), photoData)
        else:
            hash = stringToHash(photoData.photoHash())

        if hash == None:
            return

        print(f" [>] processing similar photos for photoId: {photoData.name}")
        idsOfSimilarPhotos = getIdsOfSimilarPhotos(photoData, photoCache, hash)        
        if idsOfSimilarPhotos == None or len(idsOfSimilarPhotos) == 0:
            print(f" [*] Didn't find any similar photo")
            return

    print(f" [ ] Found {len(idsOfSimilarPhotos)} similar photos to photoId {photo.id()}")
    with DictCache("similarPhoto.json", "json") as similarPhotoCache:
        similarPhotoCache.save(photo.id(), idsOfSimilarPhotos)

def getIdsOfSimilarPhotos(photo, photoCache, hash):
    idsOfSimilarPhotos = []
    for photoIdToCompareWith, photoToCompareWith in photoCache.get():
        if photoIdToCompareWith == photo.id or photoToCompareWith.photoHash() == None:
            continue

        hashOfPhotoToCompareWith = stringToHash(photoToCompareWith.photoHash())
        diff = hashOfPhotoToCompareWith - hash
        diffPercentage = (100 - diff)
        print(f" [%] Comparing photo {photo.name} with {photoToCompareWith.name} => {diff} <> {diffPercentage}")
        if diffPercentage < 80:
            continue
        idsOfSimilarPhotos.append(photoIdToCompareWith)
    return idsOfSimilarPhotos

def getPhotoHash(photoData, mediaManager):
    if photoData.hash != None:
        return stringToHash(photoData.hash)

    base_photo = GoogleMediaItem(mediaManager.get(photoData.id))
    print(f"Downloading photo {photoData.id}")
    raw_photo = downloadPhoto(base_photo)
    hash = imagehash.average_hash(raw_photo)
    raw_photo.close()
    if hash == None:
        return None
    return hash

def getInputsFromMessage(serialisedMessage):
    serialisedMessage = serialisedMessage.decode()
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
    photo_filename = photo.filename()
    download_path = os.path.join(DOWNLOAD_FOLDER, photo_filename)

    if not os.path.exists(download_path):
        with open(download_path, 'wb') as output:
            output.write(photo.raw_download())

    return getImage(download_path)


def getImage(photo_path):
    if os.path.exists(photo_path) == False:
        return None
    return Image.open(photo_path)
