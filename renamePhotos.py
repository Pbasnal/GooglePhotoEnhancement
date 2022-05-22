import os  

def renamePhotos(test_dir):
    photos = [f for f in os.listdir(
        test_dir) if os.path.isfile(test_dir + f)]

    if len(photos) <= 0:
        print(f"Nothing found in the folder {test_dir}\n{photos}")
        return 

    for photo in photos:
        photo_path = test_dir + photo
        print(f"#>  Input image: {photo_path}")
        if not photo_path.endswith(".png"):
            continue
        # iphone_orig__DSC0002_enhanced
        new_photo = photo.replace("iphone_orig__", "") \
            .replace("_enhanced", "")
        print(test_dir + new_photo)
        os.rename(photo_path, test_dir + new_photo)


photos_dir = "./DPED/visual_results/"

print(os.listdir(photos_dir))

renamePhotos(photos_dir)