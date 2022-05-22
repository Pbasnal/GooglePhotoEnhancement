import rawpy
import imageio
from PIL import Image, ImageEnhance
import numpy as np
import tensorflow as tf
from DPED.models import resnet
import DPED.utils as utils
import os
import sys

tf.compat.v1.disable_v2_behavior()
# process command arguments
phone, dped_dir, test_subset, iteration, resolution, use_gpu = utils.process_test_model_args(
    sys.argv)

dped_dir = f"DPED/{dped_dir}"
output_folder = f"DPED"
models_folder = "DPED/models_orig"


# get all available image resolutions
res_sizes = utils.get_resolutions()

# get the specified image resolution
IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_SIZE = utils.get_specified_res(
    res_sizes, phone, resolution)

# disable gpu if specified
config = tf.compat.v1.ConfigProto(
    device_count={'GPU': 0}) if use_gpu == "false" else None


test_dir = dped_dir + \
    phone.replace("_orig", "") + "/test_data/full_size_test_images/"
test_photos = [f for f in os.listdir(test_dir) if os.path.isfile(test_dir + f)]

# generate enhanced image
for photo in test_photos:
    print(f"#>  Input image: {test_dir + photo}")
    if photo.endswith(".DS_Store"):
        continue
    if photo.endswith(".NEF"): 
        raw = rawpy.imread(test_dir + photo)
        rgb = raw.postprocess()
        print(f"\n\n#>  rbg shape: {rgb.shape} {rgb.dtype}")
    else:
        rgb = imageio.imread(test_dir + photo)

    IMAGE_HEIGHT = rgb.shape[0]
    IMAGE_WIDTH = rgb.shape[1]
    photo_name = photo.rsplit(".", 1)[0]
    output_image = f"{output_folder}/visual_results/{phone}_{photo_name}_enhanced.png"

    # create placeholders for input images
    IMAGE_SIZE = IMAGE_HEIGHT * IMAGE_WIDTH * 3
    x_ = tf.compat.v1.placeholder(tf.float32, [None, IMAGE_SIZE])
    x_image = tf.reshape(x_, [-1, IMAGE_HEIGHT, IMAGE_WIDTH, 3])
    enhanced = resnet(x_image)
    with tf.compat.v1.Session(config=config) as sess:
        # load pre-trained model
        saver = tf.compat.v1.train.Saver()
        saver.restore(sess, f"{models_folder}/{phone}")
        
        print("#>  Testing original " + phone.replace("_orig", "") +
              " model, processing image " + photo)
        image = np.float16(np.array(Image.fromarray(rgb)
            .resize([IMAGE_WIDTH, IMAGE_HEIGHT]))) / 255

        image_crop = utils.extract_crop(image, resolution, phone, res_sizes)
        image_crop_2d = np.reshape(image_crop, [1, IMAGE_SIZE])

        # get enhanced image
        print(f"#>  Starting model execution")
        enhanced_2d = sess.run(enhanced, feed_dict={x_: image_crop_2d})
        enhanced_image = np.reshape(
            enhanced_2d, [IMAGE_HEIGHT, IMAGE_WIDTH, 3])
        print(f"#>  Model completed")

        # save the results as .png images
        imageio.imwrite(output_image, enhanced_image)

    image = Image.open(output_image)
    red, green, blue = image.split()

    green = ImageEnhance.Brightness(green).enhance(0.95)
    red = ImageEnhance.Brightness(red).enhance(0.9)
    blue = ImageEnhance.Brightness(blue).enhance(1.1)

    new_image = Image.merge("RGB", (red, green, blue))
    new_image = ImageEnhance.Color(new_image).enhance(0.8)
    imageio.imwrite(output_image, new_image)
