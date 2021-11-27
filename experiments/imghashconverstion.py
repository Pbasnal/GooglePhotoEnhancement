from PIL import Image
import imagehash
from imagehash import ImageHash
import os
import numpy as np

PHOTO_FOLDER = "../photos/processed/"

def getPhotoPath(photo_name):
    return PHOTO_FOLDER + photo_name

def getImage(photo_name):
    photo_path = getPhotoPath(photo_name)
    if os.path.exists(photo_path) == False:
        return None
    return Image.open(getPhotoPath(photo_name))

def imgHash(photo_name):
    image = getImage(photo_name)
    if image == None:
        return None
    return imagehash.average_hash(getImage(photo_name))

def binary_array_to_hex(arr):
	"""
	internal function to make a hex string out of a binary array.
	"""
	bit_string = ''.join(str(b) for b in 1 * arr.flatten())
	width = int(np.ceil(len(bit_string)/4))
	return '{:0>{width}x}'.format(int(bit_string, 2), width=width)


test_photos = [f for f in os.listdir(
    PHOTO_FOLDER) if os.path.isfile(PHOTO_FOLDER + f) and f != ".DS_Store"]
if len(test_photos) <= 0:
    exit()

test_photos.sort()
for p in test_photos:
    hashOfImg = imgHash(p).hash
    bit_string = ''.join(str(b) for b in 1 * hashOfImg.flatten())
    width = int(np.ceil(len(bit_string)/4))
    strhash = '{:0>{width}x}'.format(int(bit_string, 2), width=width)

    str_to_int = int(strhash, 16)
    int_to_binary = np.array([bool(int(b)) for b in "{0:0>64b}".format(str_to_int)])
    arr_to_hash = int_to_binary.reshape((8,8))
    # print(arr_to_hash)
    # bin_to_arr = np.fromstring(int_to_binary, dtype=bool, sep='')
    # print(bin_to_arr)

    hash_to_imghash = ImageHash(arr_to_hash)

    print(strhash, str_to_int, hash_to_imghash, imgHash(p) - hash_to_imghash)

    #print(binary_array_to_hex(hashOfImg))

