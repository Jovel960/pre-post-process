from db.sqlite import (getDB)
import json

def fetch_images_url():
    images = getDB().execute('select images from trainData where LENGTH(images) > 0;')
    return None
    
