import cv2
import numpy as np
import urllib.request
from io import BytesIO

def download_image(url):
    """Download an image from a URL to a numpy array suitable for OpenCV processing."""
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def merge_images_with_padding(image1, image2, output_path, horizontal=True):
    # Load the two images
    # image1 = cv2.imread(image1)
    # image2 = cv2.imread(image2)

    # Determine the size differences
    height_diff = abs(image1.shape[0] - image2.shape[0])
    width_diff = abs(image1.shape[1] - image2.shape[1])

    # Identify the smaller image and calculate padding for width and height
    if image1.shape[0] > image2.shape[0] or image1.shape[1] > image2.shape[1]:
        pad_top = height_diff // 2
        pad_bottom = height_diff - pad_top
        pad_left = width_diff // 2
        pad_right = width_diff - pad_left
        image2_padded = cv2.copyMakeBorder(image2, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        image_to_concat = (image1, image2_padded)
    else:
        pad_top = height_diff // 2
        pad_bottom = height_diff - pad_top
        pad_left = width_diff // 2
        pad_right = width_diff - pad_left
        image1_padded = cv2.copyMakeBorder(image1, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        image_to_concat = (image1_padded, image2)

    # Merge the images
    if horizontal:
        combined_image = cv2.hconcat(image_to_concat)
    else:
        combined_image = cv2.vconcat(image_to_concat)

    # Save the combined image
    cv2.imwrite(output_path, combined_image)
