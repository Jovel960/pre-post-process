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

if __name__ == "__main__":
    merge_images()
    # adjust_annotation_for_fake_image_with_all_padding(bbox=[1632.566614786784,348.4166666666667,178.5,178.50000000000006],
    #                                                   bottom_padding=151,
    #                                                   fake_height=630,
    #                                                   fake_width=811,
    #                                                   left_padding=189,
    #                                                   merged_height=630,
    #                                                   merged_width=2380,
    #                                                   right_padding=190,
    #                                                   segmentation=[[1632.566614786784,359.75,1632.566614786784,526.9166666666667,1811.066614786784,518.4166666666667,1808.2332814534507,348.4166666666667]]
    #                                                   ,top_padding=151)

