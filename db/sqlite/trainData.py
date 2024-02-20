from db.sqlite import (getDB)
import json

def fetch_images_url():
    parsed_images = []
    images = getDB().cursor().execute('select images from trainData where LENGTH(images) > 0;').fetchall()
    for imgTup in images:
        parsed_images.append(json.loads(imgTup[0]))
    return parsed_images
    
