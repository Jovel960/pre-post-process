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
    getDB().cursor().execute(query, (json.dumps(dims), id)).fetchall()
    getDB().commit()
    #

def save_adjusted_annotation(text, annotation):
    query = "update trainData set adjustedAnnotation = ? where text = ?"
    getDB().cursor().execute(query, (json.dumps(annotation), text)).fetchall()
    getDB().commit()
    #

def fetch_image_annotation(image_name):
    query = "select adjustedAnnotation from trainData where text = ?"
    adjustedAnnotation = getDB().cursor().execute(query, (image_name,)).fetchone()
    return adjustedAnnotation
    #

def clearDimsAndAnnotations():
    #change to union 
    query = "update trainData set dims = NULL where dims is not NULL"
    getDB().cursor().execute(query).fetchall()
    query = "update trainData set adjustedAnnotation = NULL where adjustedAnnotation is not NULL"
    getDB().cursor().execute(query).fetchall()
    getDB().commit()
    #
