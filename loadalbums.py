from gphotospy.album import *
from gphotospy.media import *
from authorizegoogle import getAuthorizedService
from cacheservice import FileCacheService

def getAllAlbumsFromGoogle(service):
    album_manager = Album(service)
    album_iterator = album_manager.list()

    for album in album_iterator:
        album_title = album.get('title')
        album["title"] = album_title if album_title != None else "Untitled"
        yield album

def cacheAlbumIds(googleService, cacheService):
    for album in getAllAlbumsFromGoogle(googleService):
        cacheService.save(album.get('id'), album.get('title'))
        yield album


if __name__ == "__main__":
    googleService = getAuthorizedService()
    with FileCacheService("albumCache.json", 'w') as cacheService:
        cacheAlbumIds(googleService, cacheService)