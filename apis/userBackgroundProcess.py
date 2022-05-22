import json

from gphotospy.album import *
from apis.AuthorizeWithGoogle import getGooglePhotoService
from cacheservice import DictCache
from loadalbumphotos import cachePhotoMetaData
from apis.messagebus import USER_QUEUE, PHOTO_QUEUE
from apis.messagebus import MessageBus
Bus = MessageBus()

ALBUM_PROCESS_STATUS_FILE = "albumProcessStatus.json"

class AlbumProcess:
    def __init__(self, albumId, albumName, status) -> None:
        self.albumId = albumId
        self.albumName = albumName
        self.status = status

def registerMessageListener(channel):
    print(f"Registering listener processUser")
    channel.basic_consume(
        queue=USER_QUEUE, on_message_callback=processUser, auto_ack=True)

def getAllAlbumsFromGoogle(service):
    album_manager = Album(service)
    album_iterator = album_manager.list()

    for album in album_iterator:
        album_title = album.get('title')
        album["title"] = album_title if album_title != None else "Untitled"
        yield album


def cacheAlbumProcessStatus(googleService, cacheService):
    for album in getAllAlbumsFromGoogle(googleService):
        albumProcess = AlbumProcess(album.get('id'), album.get('title'), False)
        cacheService.save(album.get('id'), albumProcess)
        yield albumProcess


def processUser(ch, method, properties, userId):
    status = None
    userId = userId.decode() 
    with DictCache("userProcessCache.json") as userProcessCache:
        status = userProcessCache.getForKey(userId)
        if status == True:
            # This means that request is already processed
            return
        if status == None:
            userProcessCache.save(userId, False)

    googleService = getGooglePhotoService(userId)
    if googleService == None:
        print(f"Couldn't create googleService for userId: {userId}")
        return

    with DictCache(ALBUM_PROCESS_STATUS_FILE) as albumProcessStatus:
        albumProcess: AlbumProcess
        for albumProcess in cacheAlbumProcessStatus(googleService, albumProcessStatus):
            print(f"Publishing album {albumProcess.albumName}")
            with DictCache("photoCache.json") as photoCache:
                print("Opened photo cache")
                for googlePhoto in cachePhotoMetaData(googleService, photoCache, albumProcess.albumId):
                    print("Publishing photo")
                    message = json.dumps({
                            "albumId": albumProcess.albumId,
                            "photo": googlePhoto,
                            "userId": userId
                        },
                        default=lambda o: o.__dict__,
                        sort_keys=True)
                    Bus.publish(PHOTO_QUEUE, message)
            albumProcess.status = True
            albumProcessStatus.save(albumProcess.albumId, albumProcess)
    print("Published all albums")
