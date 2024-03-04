import cv2
import numpy as np
import urllib.request
from io import BytesIO

def download_image(url):
    try:
        """Download an image from a URL to a numpy array suitable for OpenCV processing."""
        req = urllib.request.Request(
            url, 
            headers={
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                 })
        resp = urllib.request.urlopen(req)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f'error processing images, moving to next images, {url}')


import cv2

def merge_images_with_padding(image1, image2, output_path, horizontal=True):
    try:
        # Calculate padding differences
        height_diff = abs(image1.shape[0] - image2.shape[0])
        width_diff = abs(image1.shape[1] - image2.shape[1])
        # Initialize padding variables
        padding_info = {
            'image1': {'pad_top': 0, 'pad_bottom': 0, 'pad_left': 0, 'pad_right': 0},
            'image2': {'pad_top': 0, 'pad_bottom': 0, 'pad_left': 0, 'pad_right': 0},
        }
        pad_top, pad_bottom, pad_left, pad_right = 0, 0, 0, 0
        # Determine which image is smaller for both dimensions
        if image1.shape[0] < image2.shape[0]:
            pad_top = height_diff // 2
            pad_bottom = height_diff - pad_top
            image1 = cv2.copyMakeBorder(image1, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            padding_info['image1'].update({'pad_top': pad_top, 'pad_bottom': pad_bottom})
        else:
            pad_top = height_diff // 2
            pad_bottom = height_diff - pad_top
            image2 = cv2.copyMakeBorder(image2, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            padding_info['image2'].update({'pad_top': pad_top, 'pad_bottom': pad_bottom})

        if image1.shape[1] < image2.shape[1]:
            pad_left = width_diff // 2
            pad_right = width_diff - pad_left
            image1 = cv2.copyMakeBorder(image1, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            padding_info['image1'].update({'pad_left': pad_left, 'pad_right': pad_right})
        else:
            pad_left = width_diff // 2
            pad_right = width_diff - pad_left
            image2 = cv2.copyMakeBorder(image2, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            padding_info['image2'].update({'pad_left': pad_left, 'pad_right': pad_right})

        # Concatenate images based on the specified orientation
        if horizontal:
            combined_image = cv2.hconcat([image1, image2])
        else:
            combined_image = cv2.vconcat([image1, image2])

        # Save the combined image
        cv2.imwrite(output_path, combined_image)

        return {
            "padding_info": padding_info,
            "real_image_height": image1.shape[0],
            "real_image_width": image1.shape[1],
            "fake_image_height": image2.shape[0],
            "fake_image_width": image2.shape[1],
            "combined_image_height": combined_image.shape[0],
            "combined_image_width": combined_image.shape[1],
        }
    except Exception as e:
        print(f'Error processing images: {str(e)}')
        return {}

# Note: You should replace the placeholders `image1`, `image2`, and `output_path` with actual image data and a valid output path.

#Post process function
def adjust_annotation_for_images(segmentation, bbox, merged_width, merged_height, original_width, fake_width, fake_height, padding_info):
    """
    Adjust annotation coordinates for a fake image with padding on all sides within a merged image.
    
    Parameters:
    - segmentation: List of polygon points in the merged image.
    - bbox: Bounding box in the merged image.
    - merged_width, merged_height: Dimensions of the merged image.
    - original_width: Width of the original image, needed to calculate offset when it's padded.
    - fake_width, fake_height: Dimensions of the fake image.
    - padding_info: Dictionary containing padding values for both images.
    
    Returns:
    - Adjusted segmentation and bbox as per the standalone fake image's coordinates.
    """
    # Determine padding values
    top_padding, bottom_padding, left_padding, right_padding = padding_info['image2']['pad_top'], padding_info['image2']['pad_bottom'], padding_info['image2']['pad_left'], padding_info['image2']['pad_right']

    # Infer if the original image is padded based on its padding values
    original_image_padded = any(padding_info['image1'].values())

    # Adjust x_offset based on padding values and the width of the original image
    x_offset = original_width + (padding_info['image1']['pad_left'] if not original_image_padded else 0)

    # Adjust segmentation points
    adjusted_segmentation = []
    for polygon in segmentation:
        adjusted_polygon = []
        for i in range(0, len(polygon), 2):
            # Adjust for horizontal offset, considering left padding of the fake image
            x = polygon[i] - x_offset - left_padding 
            # Adjust for top padding of the fake image
            y = polygon[i+1] - top_padding
            adjusted_polygon.extend([x, y])
        adjusted_segmentation.append(adjusted_polygon)

    # Adjust bbox
    adjusted_bbox_x = bbox[0] - x_offset - left_padding
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