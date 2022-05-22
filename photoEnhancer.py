import json
import subprocess
import shutil
from PhotoData import PhotoData
from GoogleMediaItem import GoogleMediaItem
from authorizegoogle import getAuthorizedService
from cacheservice import DictCache
from loadalbums import cacheAlbumIds
from loadalbumphotos import cachePhotoMetaOfAlbum
from gphotospy.media import *

DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"
ENHANCED_PHOTO_FOLDER = "DPED/dped/iphone/test_data"

def loadListOfAlbumsFromCache(googleService, force_refresh_cache=False):
    if force_refresh_cache:
        with DictCache("albumCache.json") as albumCacheService:
            cacheAlbumIds(googleService, albumCacheService)

    albumTitleIdMap = dict()
    with DictCache("albumCache.json") as albumCacheService:
        for id, data in albumCacheService.get():
            if not id.strip():
                continue
            albumTitleIdMap[data] = id

    return albumTitleIdMap


def selectAnAlbumToEnhance(albumIdMap):
    print("Select an album to enhance")
    i = 1
    album_titles = list(albumIdMap.keys())
    for title in album_titles:
        print(f"{i}> {title}")
        i += 1
    selectedAlbumIndex = int(input("Which album # > "))

    albumTitle = album_titles[selectedAlbumIndex - 1]
    print(f"Selected album \"{albumTitle}\"")

    return albumIdMap[albumTitle]


def loadPhotoIdsOfAlbum(googleService, albumId, force_refresh_photoid_map=False):
    print(f"albumId> {albumId}")
    if force_refresh_photoid_map:
        with DictCache("albumPhotoMapCache.json") as albumPhotoMapCache:
            with DictCache("photoCache.json") as photoCache:
                cachePhotoMetaOfAlbum(
                    googleService, albumPhotoMapCache, photoCache, albumId)

    with DictCache("albumPhotoMapCache.json") as albumPhotoMapCacheService:
        for cacheKey, line in albumPhotoMapCacheService.get():
            # print(f"\nKey: {cacheKey} \n<> Data: {line}")
            albumPhotoMap = json.loads(line)
            if cacheKey == albumId:
                return albumPhotoMap

    return []


def getAlbumIdMap(googleService):
    albumIdMap = loadListOfAlbumsFromCache(googleService)
    if bool(albumIdMap) == False:
        albumIdMap = loadListOfAlbumsFromCache(googleService, True)

    if bool(albumIdMap) == False:
        print(f"No album Id to process photos of")
        return None

    return selectAnAlbumToEnhance(albumIdMap)


def getPhotoIds(googleService, ablumId):
    photoIds = loadPhotoIdsOfAlbum(googleService, ablumId)
    if len(photoIds) == 0:
        photoIds = loadPhotoIdsOfAlbum(googleService, ablumId, True)

    if len(photoIds) == 0:
        print("Photos of selected album doesn't have any photos")

    return photoIds


def enhancePhoto(photo: GoogleMediaItem):
    photo_filename = photo.filename()
    if  photo.mimeType().find("jpeg") != -1:
        photo_filename = photo_filename.replace("NEF", "jpg")
    
    download_path = os.path.join(DOWNLOAD_FOLDER, photo_filename)

    with open(download_path, 'wb') as output:
        output.write(photo.raw_download())

    if download_path == None:
        print(f"Failed to download the photo {photo.filename()}")
        return

    # * running the model as a separate process because calling the function directly
    # * fails for images of different dimensions. Once that issue is fixed, we call
    # * directly calll the processPhoto method.
    print(f"\n\n Enhancing photo {photo.filename()}")
    command = "python runmodel.py model=iphone_orig test_subset=full".split()
    process = subprocess.run(command, capture_output=True, text=True)

    print(
        f"runmodel stdout> {process.stdout} \nrunmodel stderr> {process.stderr}\n")
    print(f"runmodel returncode> {process.returncode}")

    photoData = PhotoData(photo.id(), 
                        photo_filename,
                        photo.metadata()["height"],
                        photo.metadata()["width"],
                        True)
    with DictCache("photoCache.json") as photoCache:
        # print(photoData.toString())
        photoCache.save(photo.id(), photoData)

    enhancedPhotoPath = os.path.join(ENHANCED_PHOTO_FOLDER, photo.filename())
    shutil.move(download_path, enhancedPhotoPath)


def main():

    googleService = getAuthorizedService()

    albumIdToEnhance = getAlbumIdMap(googleService)
    if albumIdToEnhance == None:
        exit()

    photoIds = getPhotoIds(googleService, albumIdToEnhance)
    if len(photoIds) == 0:
        print("There are no photos for this album")
        exit()

    mediaManager = Media(googleService)
    for photoId in photoIds:
        base_photo = mediaManager.get(photoId)
        photo = GoogleMediaItem(base_photo)
        enhancePhoto(photo)
        break


if __name__ == "__main__":
    main()
