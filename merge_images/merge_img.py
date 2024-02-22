import cv2
import numpy as np
import urllib.request
from io import BytesIO

def download_image(url):
    try:
        """Download an image from a URL to a numpy array suitable for OpenCV processing."""
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print('error processing images, moving to next images')


def merge_images_with_padding(image1, image2, output_path, horizontal=True):
    # Load the two images
    # image1 = cv2.imread(image1)
    # image2 = cv2.imread(image2)
    try:
        image2_original_height, image2_original_width = image2.shape[:2]
        # Determine the size differences
        height_diff = abs(image1.shape[0] - image2.shape[0])
        width_diff = abs(image1.shape[1] - image2.shape[1])

        pad_top, pad_right, pad_bottom, pad_left = 0, 0, 0, 0
        fakeImagePadded = False

        # Identify the smaller image and calculate padding for width and height
        if image1.shape[0] > image2.shape[0] or image1.shape[1] > image2.shape[1]:
            fakeImagePadded = True
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

        combined_height, combined_width = combined_image.shape[:2]
        # Save the combined image
        cv2.imwrite(output_path, combined_image)
        if fakeImagePadded:
            return { "fake_image_height":image2_original_height, 
                "fake_image_width":image2_original_width, 
                "combined_image_height":combined_height, 
                "combined_image_width":combined_width,
                "pad_top":pad_top,
                "pad_bottom":pad_bottom,
                "pad_left":pad_left,
                "pad_right":pad_right } 
        return { "fake_image_height":image2_original_height, 
                "fake_image_width":image2_original_width, 
                "combined_image_height":combined_height, 
                "combined_image_width":combined_width }
    except Exception as e:
        print('error processing images, moving to next images')

def extract_fake_image(merged_image_path, fake_image_width, fake_image_height, output_path='extracted_image2.jpg'):
    # Load the merged image
    merged_image = cv2.imread(merged_image_path)

    # Assuming image2 is on the right and using its dimensions to extract it
    start_col = merged_image.shape[1] - fake_image_width  # Start column for image2

    # Extract the right image based on its original dimensions
    fake_image_extracted = merged_image[:fake_image_height, start_col:start_col + fake_image_width]
    
    # Save the extracted image as a file
    cv2.imwrite(output_path, fake_image_extracted )
    # return image2_extracted