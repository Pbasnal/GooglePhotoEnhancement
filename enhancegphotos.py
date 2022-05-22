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

def download_file(url: str, destination_folder: str, file_name: str):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(destination_folder, file_name)
        print('Downloading file {0}'.format(file_path))

        with open(file_path, 'wb') as f:
            f.write(response.content)
            f.close()


media_manager = Media(service)
photo_iterator = media_manager.search(MEDIAFILTER.PHOTO)
image_scale = 1
i = 0
for photo in photo_iterator:
    photo_name = photo.get("filename")
    photo_height = photo.get("mediaMetadata").get("height")
    photo_width = photo.get("mediaMetadata").get("width")
    photo_type = photo.get("mediaMetadata").get("mimeType")
    photo_base_url = photo.get("baseUrl")

    download_folder = "DPED/dped/iphone/test_data/full_size_test_images"
    test_folder = "DPED/dped/iphone/test_data"

    download_file(photo_base_url + "=d", download_folder, photo_name)

    # processPhoto("model=iphone_orig test_subset=full".split(), image_scale)

    # * running the model as a separate process because calling the function directly
    # * fails for images of different dimensions. Once that issue is fixed, we call
    # * directly calll the processPhoto method.
    command = "python runmodel.py model=iphone_orig test_subset=full".split()
    process = subprocess. run(command, capture_output=True, text=True)

    print(f"{photo_name} | {photo_width}x{photo_height} | {photo_type}")
    print(f"\n\n Enhancing photo {photo_name}")
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)

    file_path = os.path.join(download_folder, photo_name)
    test_path = os.path.join(test_folder, photo_name)
    shutil.move(file_path, test_path)

    i += 1
    if i == 5:
        break
