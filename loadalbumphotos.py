# * This file is an experiment file
from GoogleMediaItem import GoogleMediaItem
from PhotoData import PhotoData
from gphotospy.album import *
from gphotospy.media import *
from authorizegoogle import getAuthorizedService
from cacheservice import CacheService, FileCacheService

def getAllPhotosFromGoogle(service, album_id):
    media_manager = Media(service)
    media_iterator = media_manager.search_album(album_id)
    
    for media in media_iterator:
        media_item = GoogleMediaItem(media)
        if not media_item.is_photo():
            continue
        yield media_item


def cachePhotoIds(googleService, cacheService : CacheService, album_id):
    for googlePhoto in getAllPhotosFromGoogle(googleService, album_id):

        photoData = PhotoData(googlePhoto.id(), 
                    googlePhoto.filename(),
                    googlePhoto.metadata()["height"],
                    googlePhoto.metadata()["width"],
                    False)

        cacheService.save(photoData.id, photoData)

        yield googlePhoto

def cachePhotoMetaOfAlbum(googleService, albumPhotoCache, photoCache, album_id):
    print("Starting photo caching")

    photoIds = []
    for googlePhoto in cachePhotoIds(googleService, photoCache, album_id):
        photoIds.append(googlePhoto.id())
    
    albumPhotoCache.save(album_id, json.dumps(photoIds), is_json=True)

if __name__ == "__main__":
    googleService = getAuthorizedService()
    print("got authorized google service")
    album_id = "AJ36JaTc-eVoeViRkl9tomz_XYebkpOqYy9ijNSr7u3SlrgjjbW2jhb0Dn3hAEkldWvatMPOxvoi"

    with FileCacheService("albumPhotoMapCache.json", 'w') as albumPhotoCacheService:
        with FileCacheService("photoCache.json", 'w') as photoCacheService:
            cachePhotoMetaOfAlbum(googleService, album_id)