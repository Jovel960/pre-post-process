import db
from merge_images import (merge_images_with_padding, download_image, extract_fake_image, adjust_annotation_for_fake_image_with_all_padding)
import json

#Pre processing
def merge_images():
    dbRes = db.fetch_images_url()

    for i in range(len(dbRes)):
         if 'original' in dbRes[i]['images'] and 'manipulated' in dbRes[i]['images']:
            realImg = download_image(dbRes[i]["images"]["original"])
            fakeImage = download_image(dbRes[i]["images"]["manipulated"])
            if realImg is not None and fakeImage is not None and realImg.any() and fakeImage.any():
                realImageDims = merge_images_with_padding(image1=realImg, image2=fakeImage, output_path=rf"C:\Users\User\.vscode\merge_images\images\{dbRes[i]['id']}.png")
                db.save_dims(id=dbRes[i]['id'], dims=realImageDims)
