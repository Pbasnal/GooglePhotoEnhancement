import json
import subprocess
import shutil
from GoogleMediaItem import GoogleMediaItem
from authorizegoogle import getAuthorizedService
from cacheservice import FileCacheService
from loadalbums import cacheAlbumIds
from loadalbumphotos import cachePhotoMetaOfAlbum
from gphotospy.media import *

DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"
ENHANCED_PHOTO_FOLDER = "DPED/dped/iphone/test_data"

def loadListOfAlbumsFromCache(googleService, force_refresh_cache=False):
    if force_refresh_cache:
        with FileCacheService("albumCache.json", 'a+') as albumCacheService:
            cacheAlbumIds(googleService, albumCacheService)

    albumTitleIdMap = dict()
    with FileCacheService("albumCache.json", 'r') as albumCacheService:
        for line in albumCacheService.get():
            album_info = json.loads(line)
            albumTitleIdMap[album_info.get("data")] = album_info.get("id")

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
        with FileCacheService("albumPhotoMapCache.json", 'a+') as albumPhotoMapCacheService:
            with FileCacheService("photoCache.json", 'w') as photoCacheService:
                cachePhotoMetaOfAlbum(googleService, albumPhotoMapCacheService, photoCacheService, albumId)

    with FileCacheService("albumPhotoMapCache.json", 'r') as albumPhotoMapCacheService:
        for line in albumPhotoMapCacheService.get():
            albumPhotoMap = json.loads(line)
            if albumPhotoMap.get("id") == albumId:
                return albumPhotoMap.get("data")

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
    download_path = os.path.join(DOWNLOAD_FOLDER, photo.filename())

    with open(download_path, 'wb') as output:
        output.write(photo.raw_download())

    # * running the model as a separate process because calling the function directly
    # * fails for images of different dimensions. Once that issue is fixed, we call
    # * directly calll the processPhoto method.    
    print(f"\n\n Enhancing photo {photo.filename()}")
    command = "python runmodel.py model=iphone_orig test_subset=full".split()
    process = subprocess.run(command, capture_output=True, text=True)

    print(f"runmodel stdout> {process.stdout} \nrunmodel stderr> {process.stderr}\n")
    print(f"runmodel returncode> {process.returncode}")

    enhancedPhotoPath = os.path.join(ENHANCED_PHOTO_FOLDER, photo.filename())
    shutil.move(download_path, enhancedPhotoPath)


def main():

    googleService = getAuthorizedService()

    albumIdToEnhance = getAlbumIdMap(googleService)
    if albumIdToEnhance == None:
        exit()

    photoIds = getPhotoIds(googleService, albumIdToEnhance)
    if len(photoIds) == 0:    
        exit()

    mediaManager  = Media(googleService)
    for photoId in photoIds:
        photo = GoogleMediaItem(mediaManager.get(photoId))
        enhancePhoto(photo)

if __name__ == "__main__":
    main()
