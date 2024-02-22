import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

def visualize_annotations(image_path, segmentation, bbox):
    # Load the image
    img = Image.open(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    
    # Draw segmentation polygons
    for polygon in segmentation:
        poly_points = np.array(polygon).reshape((-1, 2))  # Reshape to Nx2 array
        poly = patches.Polygon(poly_points, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(poly)
    
    # Draw bounding box
    rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1, edgecolor='g', facecolor='none')
    ax.add_patch(rect)
    
    plt.axis('off')  # Optional: Hide axis for better visualization
    plt.show()