import rawpy
import imageio
from PIL import Image, ImageEnhance
import numpy as np
import tensorflow as tf
from DPED.models import resnet
from DPED import utils
import os
import sys

tf.compat.v1.disable_v2_behavior()


def processPhoto(arguments, image_scale=1):
    # process command arguments
    # phone, dped_dir, test_subset, iteration, resolution, use_gpu = utils.process_test_model_args(sys.argv)
    phone, dped_dir, _, _, _, use_gpu = utils.process_test_model_args(
        arguments)
    dped_dir = "DPED/" + dped_dir
    # disable gpu if specified
    config = tf.compat.v1.ConfigProto(
        device_count={'GPU': 0}) if use_gpu == "false" else None

    test_dir = dped_dir + \
        phone.replace("_orig", "") + "/test_data/full_size_test_images/"
    photo_name_with_extension, photo_data = getPhotoToEnhance(test_dir)

    photo_name = photo_name_with_extension.rsplit(".", 1)[0]
    output_image = "DPED/visual_results/" + phone + "_" + photo_name + "_enhanced.png"

    enhanced_image = runModelEnhancement(config,
                                         photo_data,
                                         image_scale,
                                         phone,
                                         photo_name_with_extension)

    enhanced_image = applyCustomEnhancements(output_image, enhanced_image)

    imageio.imwrite(output_image, enhanced_image)


def applyCustomEnhancements(output_image_path, image):
    # save the results as .png images
    imageio.imwrite(output_image_path, image)

    image = Image.open(output_image_path)
    red, green, blue = image.split()

    green = ImageEnhance.Brightness(green).enhance(0.95)
    red = ImageEnhance.Brightness(red).enhance(0.9)
    blue = ImageEnhance.Brightness(blue).enhance(1.1)

    enhance_image = Image.merge("RGB", (red, green, blue))
    enhance_image = ImageEnhance.Color(enhance_image).enhance(0.8)

    return enhance_image


def runModelEnhancement(config, photo_data, image_scale, phone, photo_name_with_extension):
    IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_SIZE = getImageDimensions(
        photo_data, image_scale)

    model_input, model = getModel(IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_SIZE)
    with tf.compat.v1.Session(config=config) as sess:
        # load pre-trained model
        saver = tf.compat.v1.train.Saver()
        saver.restore(sess, "DPED/models_orig/" + phone)

        print("#>  Testing original " + phone.replace("_orig", "") +
              " model, processing image " + photo_name_with_extension)

        model_input_image = getModelInput(
            IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_SIZE, photo_data)
        # get enhanced image
        print(f"#>  Starting model execution (h, w, s)",
              IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_SIZE)
        enhanced_2d = sess.run(
            model, feed_dict={model_input: model_input_image})
        enhanced_image = np.reshape(
            enhanced_2d, [IMAGE_HEIGHT, IMAGE_WIDTH, 3])
        print(f"#>  Model completed")

    return enhanced_image


def getModelInput(image_height, image_width, image_size, photo_data):
    image_in_array_form = Image.fromarray(photo_data)
    image_array_reshaped = image_in_array_form.resize(
        [image_width, image_height])
    image = np.float16(np.array(image_array_reshaped)) / 255

    return np.reshape(image, [1, image_size])


def getModel(image_height, image_width, image_size):
    model_input = tf.compat.v1.placeholder(tf.float32, [None, image_size])
    model_input_image = tf.reshape(
        model_input, [-1, image_height, image_width, 3])
    model = resnet(model_input_image)

    return model_input, model

# Currently this method will process 1 photo at a time.


def getPhotoToEnhance(test_dir):
    test_photos = [f for f in os.listdir(
        test_dir) if os.path.isfile(test_dir + f)]
    if len(test_photos) <= 0:
        return None, None

    for photo in test_photos:
        print(f"#>  Input image: {test_dir + photo}")
        if photo.endswith(".NEF"):
            raw = rawpy.imread(test_dir + photo)
            rgb = raw.postprocess()
            print(f"\n\n#>  rbg shape: {rgb.shape} {rgb.dtype}")
        elif photo.endswith(".jpg") or photo.endswith(".jpeg") or photo.endswith(".png"):
            rgb = imageio.imread(test_dir + photo)
        else:
            continue

        return photo, rgb


def getImageDimensions(photo_data, image_scale):
    image_height = np.int32(photo_data.shape[0] * image_scale)
    image_width = np.int32(photo_data.shape[1] * image_scale)
    image_size = np.int32(image_height * image_width * 3)

    return image_height, image_width, image_size


if __name__ == "__main__":
    processPhoto(sys.argv, 0.5)
