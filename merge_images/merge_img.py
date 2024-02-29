import cv2
import numpy as np
import urllib.request
from io import BytesIO

def download_image(url):
    try:
        """Download an image from a URL to a numpy array suitable for OpenCV processing."""
        resp = urllib.request.urlopen(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(url)
        print(f'error processing images, moving to next images, {e}')


def merge_images_with_padding(image1, image2, output_path, horizontal=True):
    # Load the two images
    # image1 = cv2.imread(image1)
    # image2 = cv2.imread(image2)
    try:
        # Determine the size differences
        image1_original_height, image1_original_width = image1.shape[:2]
        image2_original_height, image2_original_width = image2.shape[:2]
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
            image_to_concat = ( image1_padded, image2)

        # Merge the images
        if horizontal:
            combined_image = cv2.hconcat(image_to_concat)
        else:
            combined_image = cv2.vconcat(image_to_concat)

        combined_height, combined_width = combined_image.shape[:2]

        # Save the combined image
        cv2.imwrite(output_path, combined_image)
        # if fakeImagePadded:
        return { 
                "is_real_image_padded" : not fakeImagePadded,
                "real_image_height" : image1_original_height,
                "real_image_width" : image1_original_width,
                "fake_image_height":image2_original_height, 
                "fake_image_width":image2_original_width, 
                "combined_image_height":combined_height, 
                "combined_image_width":combined_width,
                "pad_top":pad_top,
                "pad_bottom":pad_bottom,
                "pad_left":pad_left,
                "pad_right":pad_right } 
        # return { "fake_image_height":image2_original_height, 
        #         "fake_image_width":image2_original_width, 
        #         "combined_image_height":combined_height, 
        #         "combined_image_width":combined_width }
    except Exception as e:
        print(f'error processing images, {e}')
        return {}

#Post process function
def adjust_annotation_for_images(segmentation, bbox, merged_width, merged_height, original_width, fake_width, fake_height, top_padding=0, bottom_padding=0, left_padding=0, right_padding=0, original_image_padded=False):
    """
    Adjust annotation coordinates for a fake image with padding on all sides within a merged image, considering whether the original image is padded.
    
    Parameters:
    - segmentation: List of polygon points in the merged image.
    - bbox: Bounding box in the merged image.
    - merged_width, merged_height: Dimensions of the merged image.
    - original_width: Width of the original image, needed to calculate offset when it's padded.
    - fake_width, fake_height: Dimensions of the fake image.
    - top_padding, bottom_padding, left_padding, right_padding: Padding values.
    - original_image_padded: Boolean flag indicating if the original image is padded.
    
    Returns:
    - Adjusted segmentation and bbox as per the standalone fake image's coordinates.
    """
    # Adjust x_offset based on whether the original image is padded
    if original_image_padded:
        # When the original image is padded, the starting point of the fake image is just after the original image's width
        x_offset = merged_width - original_width - left_padding - top_padding 
    else:
        # Calculate the offset from the right edge when the fake image or neither image is specifically padded
        x_offset = merged_width - fake_width - right_padding

    # Adjust segmentation points
    adjusted_segmentation = []
    for polygon in segmentation:
        adjusted_polygon = []
        for i in range(0, len(polygon), 2):
            # Adjust for horizontal offset, considering only right padding if the original image is not padded
            x = polygon[i] - x_offset
            # Adjust for top padding
            if original_image_padded:
                y = polygon[i+1] - top_padding + bottom_padding
            else: y = polygon[i+1] - top_padding
            adjusted_polygon.extend([x, y])
        adjusted_segmentation.append(adjusted_polygon)

    # Adjust bbox
    adjusted_bbox_x = bbox[0] - x_offset
    adjusted_bbox_y = bbox[1] - top_padding
    adjusted_bbox = [adjusted_bbox_x, adjusted_bbox_y, bbox[2], bbox[3]]

    return adjusted_segmentation, adjusted_bbox



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