def are_points_within_bounds(segmentation, image_width, image_height):
    for polygon in segmentation:
        for i in range(0, len(polygon), 2):
            x, y = polygon[i], polygon[i+1]
            if not (0 <= x <= image_width and 0 <= y <= image_height):
                return False
    return True

def is_bbox_valid(bbox, segmentation):
    x_min, y_min, width, height = bbox
    x_max, y_max = x_min + width, y_min + height
    
    for polygon in segmentation:
        for i in range(0, len(polygon), 2):
            x, y = polygon[i], polygon[i+1]
            if not (x_min <= x <= x_max and y_min <= y <= y_max):
                return False
    return True

def run_validation():
    pass