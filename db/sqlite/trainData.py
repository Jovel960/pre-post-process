from db.sqlite import (getDB)
import json

def fetch_images_url():
    parsed_images = []
    images = getDB().cursor().execute('select id, images, text from trainData where LENGTH(images) > 0;').fetchall()
    for imgTup in images:
        parsed_images.append({"id":imgTup[0] ,"images":json.loads(imgTup[1]), "text":imgTup[2]})
    return parsed_images
    #

def save_dims(id, dims):
    query = "update trainData set dims = ? where id = ?"
    getDB().cursor().execute(query, (json.dumps(dims), id))
    getDB().commit()
    #

def fetch_dims(id):
    query = "select dims from trainData where id = ?"
    dims = getDB().cursor().execute(query, (id,)).fetchone()
    return dims
    #

def save_adjusted_annotations(id, annotations):
    query = "update trainData set adjustedAnnotations = ? where id = ?"
    getDB().cursor().execute(query, (json.dumps(annotations), id))
    getDB().commit()
    #

def fetch_image_annotations(image_id):
    query = "select adjustedAnnotations from trainData where id = ?"
    adjustedAnnotation = getDB().cursor().execute(query, (image_id,)).fetchone()
    return adjustedAnnotation
    #

def clearDimsAndAnnotations():
    #change to union 
    query = "update trainData set dims = NULL where dims is not NULL"
    getDB().cursor().execute(query).fetchall()
    query = "update trainData set adjustedAnnotations = NULL where adjustedAnnotation is not NULL"
    getDB().cursor().execute(query).fetchall()
    getDB().commit()
    #
