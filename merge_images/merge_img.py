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
        # Determine the size differences
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
            # pad_top = height_diff // 2
            # pad_bottom = height_diff - pad_top
            # pad_left = width_diff // 2
            # pad_right = width_diff - pad_left
            # image1_padded = cv2.copyMakeBorder(image1, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            image_to_concat = (image1, image2)

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
        print(f'error processing images, {e}')
        return {}

#Post process function
def adjust_annotation_for_fake_image_with_all_padding(segmentation, bbox, merged_width, merged_height, fake_width, fake_height, top_padding=0, bottom_padding=0, left_padding=0, right_padding=0):
    """
    Adjust annotation coordinates for a fake image with padding on all sides within a merged image.
    
    Parameters:
    - segmentation: List of polygon points in the merged image.
    - bbox: Bounding box in the merged image.
    - merged_width, merged_height: Dimensions of the merged image.
    - fake_width, fake_height: Dimensions of the fake image.
    - top_padding, bottom_padding: Vertical padding values.
    - left_padding, right_padding: Horizontal padding values.
    
    Returns:
    - Adjusted segmentation and bbox as per the standalone fake image's coordinates.
    """
    # Calculate effective horizontal offset including left padding
    x_offset = merged_width - fake_width - left_padding - right_padding

    # Adjust segmentation points
    adjusted_segmentation = []
    for polygon in segmentation:  # Iterate over each polygon
        adjusted_polygon = []
        for i in range(0, len(polygon), 2):  # Iterate over pairs of coordinates
            x = polygon[i] - x_offset - left_padding  # Adjust for horizontal offset and left padding
            y = polygon[i+1] - top_padding  # Adjust for top padding
            adjusted_polygon.extend([x, y])  # Append adjusted coordinates
        adjusted_segmentation.append(adjusted_polygon)

    # Adjust bbox
    bbox_x, bbox_y, bbox_w, bbox_h = bbox
    adjusted_bbox_x = bbox_x - x_offset - left_padding  # Adjust for horizontal offset and left padding
    adjusted_bbox_y = bbox_y - top_padding  # Adjust for top padding
    adjusted_bbox = [adjusted_bbox_x, adjusted_bbox_y, bbox_w, bbox_h]

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