from db.sqlite import (getDB)
import json

def fetch_images_url():
    parsed_images = []
    images = getDB().cursor().execute('select id, images from trainData where LENGTH(images) > 0;').fetchall()
    for imgTup in images:
        print(imgTup)
        parsed_images.append({"id":imgTup[0] ,"images":json.loads(imgTup[1])})
    return parsed_images

def save_real_img_dim(id, dims):
    query = "update trainData set fakeImgDim = ? where id = ?"
    getDB().cursor().execute(query, (json.dumps(dims), id)).fetchall()
    getDB().commit()
    

