import rawpy
import imageio
import os

test_dir = "DPED/dped/iphone/test_data/full_size_test_images/"
test_photos = [f for f in os.listdir(test_dir) if os.path.isfile(test_dir + f)]

# generate enhanced image
for photo in test_photos:
    print(f"#>  Input image: {test_dir + photo}")
    if photo.endswith(".DS_Store"):
        continue
    if photo.endswith(".NEF"): 
        raw = rawpy.imread(test_dir + photo)
        rgb = raw.postprocess()
    else:
        rgb = imageio.imread(test_dir + photo)
    print(f"\n\n#>  rbg shape: {rgb.shape} {rgb.dtype}")