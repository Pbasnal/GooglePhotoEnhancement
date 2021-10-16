# * This file is an experiment file

from GoogleMediaItem import GoogleMediaItem
from gphotospy.album import *
from gphotospy.media import *
from authorizegoogle import getAuthorizedService
from cacheservice import FileCacheService

def getAllPhotosFromGoogle(service, album_id):
    media_manager = Media(service)
    media_iterator = media_manager.search_album(album_id)
    
    for media in media_iterator:
        media_item = GoogleMediaItem(media)
        if not media_item.is_photo():
            continue
        yield media_item


def cachePhotoIds(googleService, cacheService, album_id):
    for googlePhoto in getAllPhotosFromGoogle(googleService, album_id):
        id = googlePhoto.id()
        photo_name = googlePhoto.filename()
        photo_height = googlePhoto.metadata()["height"]
        photo_width = googlePhoto.metadata()["width"]

        id_json = f"\"id\": \"{id}\""
        name_json = f"\"name\": \"{photo_name}\""
        height_json = f"\"height\": \"{photo_height}\""
        width_json = f"\"width\": \"{photo_width}\""

        photo_json = f"{{ {id_json}, {name_json}, {height_json}, {width_json} }}"
        cacheService.save(id, photo_json, is_json=True)

        yield googlePhoto

def cachePhotoMetaOfAlbum(googleService, albumPhotoCacheService, photoCacheService, album_id):
    print("Starting photo caching")

    photoIds = []
    for googlePhoto in cachePhotoIds(googleService, photoCacheService, album_id):
        photoIds.append(googlePhoto.id())
    
    albumPhotoCacheService.save(album_id, json.dumps(photoIds), is_json=True)

if __name__ == "__main__":
    googleService = getAuthorizedService()
    print("got authorized google service")
    album_id = "AJ36JaTc-eVoeViRkl9tomz_XYebkpOqYy9ijNSr7u3SlrgjjbW2jhb0Dn3hAEkldWvatMPOxvoi"

    with FileCacheService("albumPhotoMapCache.json", 'w') as albumPhotoCacheService:
        with FileCacheService("photoCache.json", 'w') as photoCacheService:
            cachePhotoMetaOfAlbum(googleService, album_id)