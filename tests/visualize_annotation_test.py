import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import db
import json
import os
images_folder_path = "images"

def visualize_annotations():
    image_id = input("What is the image name you want to visuallize ?")
    print(image_id)
    adjustedAnnotation = json.loads(db.fetch_image_annotation(image_id.strip())[0])
    segmentation = adjustedAnnotation["annotations"]
    bbox = adjustedAnnotation["bbox"]
    image_path = input("What is the image path you want to visuallize ?")
    # listDir = os.listdir(images_folder_path)
    # if len(listDir):
    #     for imgFile in listDir:
    #         if image_id == imgFile.rsplit('.', 1)[0]:
    #             image_path = os.path.join(images_folder_path, imgFile)
    #             break  # Exit the loop if a match is found
    # else:
    #     print("images folder is empty")
    #     return None

    # Load the image
    img = Image.open(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    
    # Draw segmentation polygons
    for polygon in segmentation:
        poly_points = np.array(polygon).reshape((-1, 2))  # Reshape to Nx2 array
        poly = patches.Polygon(poly_points, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(poly)
    
    # #Draw bounding box
    # rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1, edgecolor='g', facecolor='none')
    # ax.add_patch(rect)
    
    plt.axis('off')  # Optional: Hide axis for better visualization
    plt.show()