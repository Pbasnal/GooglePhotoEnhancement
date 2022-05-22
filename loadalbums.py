# * This file is an experiment file

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


if __name__ == "__main__":
    googleService = getAuthorizedService()
    with FileCacheService("albumCache.json", 'w') as cacheService:
        cacheAlbumIds(googleService, cacheService)



# media_manager = Media(service)
# media_iterator = media_manager.search_album(str(selected_album_id))

# i = 0
# for media in media_iterator:
#     id = media["id"]
#     # print(media)
#     media = MediaItem(media)
#     # print(media)
#     if not media.is_photo():
#         continue

#     photo_name = media.filename()
#     photo_height = media.metadata()["height"]
#     photo_width = media.metadata()["width"]
#     print(f"{id} | {photo_name} | {photo_width}x{photo_height} ")
#     i += 1
#     if i >= 2:
#         break


# exit()

# photo_iterator = media_manager.search(MEDIAFILTER.PHOTO)
# for photo in photo_iterator:
#     photo_name = photo.get("filename")
#     photo_height = photo.get("mediaMetadata").get("height")
#     photo_width = photo.get("mediaMetadata").get("width")
#     photo_type = photo.get("mediaMetadata").get("mimeType")
#     photo_base_url = photo.get("baseUrl")

#     print(f"{photo_name} | {photo_width}x{photo_height} | {photo_type}")
