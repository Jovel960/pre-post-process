import db
from merge_images import (merge_images_with_padding, download_image, extract_fake_image, adjust_annotation_for_fake_image_with_all_padding)
import json

def merge_images():
    dbRes = db.fetch_images_url()

    for i in range(len(dbRes)):
         if 'original' in dbRes[i]['images'] and 'manipulated' in dbRes[i]['images']:
            realImg = download_image(dbRes[i]["images"]["original"])
            fakeImage = download_image(dbRes[i]["images"]["manipulated"])
            if realImg is not None and fakeImage is not None and realImg.any() and fakeImage.any():
                realImageDims = merge_images_with_padding(image1=realImg, image2=fakeImage, output_path=rf"C:\Users\User\.vscode\merge_images\images\{dbRes[i]['id']}.png")
                db.save_dims(id=dbRes[i]['id'], dims=realImageDims)

if __name__ == "__main__":
    merge_images()
    # adjust_annotation_for_fake_image_with_all_padding(bbox=[1059.4285365513392,234.28571428571428,281.9047619047619,123.8095238095238],
    #                                                   bottom_padding=0,
    #                                                   fake_height=600,
    #                                                   fake_width=800,
    #                                                   left_padding=0,
    #                                                   merged_height=600,
    #                                                   merged_width=1600,
    #                                                   right_padding=0,
    #                                                   segmentation=[[1059.4285365513392,241.9047619047619,1070.8571079799106,358.0952380952381,1341.3332984561011,348.57142857142856,1337.5237746465773,234.28571428571428]]
    #                                                   ,top_padding=0)

