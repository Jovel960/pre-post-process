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
    # adjust_annotation_for_fake_image_with_all_padding(bbox=[571.6571219308036,378.85714285714283,69.71428571428567,93.71428571428572],
    #                                                   bottom_padding=144,
    #                                                   fake_height=530,
    #                                                   fake_width=315,
    #                                                   left_padding=46,
    #                                                   merged_height=530,
    #                                                   merged_width=630,
    #                                                   right_padding=46,
    #                                                   segmentation=[[766.6030327506122,333.015332197615,1244.9675983383465,321.9761499148211,1257.8466443349394,796.6609880749575,794.2009884575968,778.2623509369677]]
    #                                                   ,top_padding=144)

