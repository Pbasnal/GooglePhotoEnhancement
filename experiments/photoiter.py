# * This file is an experiment file

import tkinter as tk
import requests
import subprocess
import os
import shutil
from gphotospy import authorize
from gphotospy.album import *
from gphotospy.media import *

CLIENT_SECRET_FILE = "google_secret_desktop.json"
service = authorize.init(CLIENT_SECRET_FILE)

DOWNLOAD_FOLDER = "DPED/dped/iphone/test_data/full_size_test_images"
PROCESSED_FOLDER = "DPED/dped/iphone/test_data"

album_manager = Album(service)
media_manager = Media(service)

album_iterator = album_manager.list()

print("Fetching albums")

album_to_enhance = "College Diaries - FE"
selected_album_id = ""
with open("albums.txt", "w") as album_list_file:
    for album in album_iterator:
        album_title = album.get('title')
        album_title = album_title if album_title != None else "Untitled"
        album_id = album.get('id')

        if album_title == album_to_enhance:
            print("found the album")
            selected_album_id = album_id

        album_list_file.write(f"{album_title}\n{album_id}\n")
        #print(f"title: {album_title} Id: {album_id}")
    album_list_file.close()

print(selected_album_id)
# album = album_manager.get(selected_album_id)
media_iterator = media_manager.search_album(str(selected_album_id))

i = 0
for media in media_iterator:
    media = MediaItem(media)
    if not media.is_photo():
        continue

    photo_name = media.filename()
    photo_height = media.metadata()["height"]
    photo_width = media.metadata()["width"]

    print(f"{photo_name} | {photo_width}x{photo_height} ")
    i += 1
    if i >= 2:
        break


exit()

photo_iterator = media_manager.search(MEDIAFILTER.PHOTO)
for photo in photo_iterator:
    photo_name = photo.get("filename")
    photo_height = photo.get("mediaMetadata").get("height")
    photo_width = photo.get("mediaMetadata").get("width")
    photo_type = photo.get("mediaMetadata").get("mimeType")
    photo_base_url = photo.get("baseUrl")

    print(f"{photo_name} | {photo_width}x{photo_height} | {photo_type}")
