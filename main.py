import db
from merge_images import (merge_images_with_padding, download_image, extract_fake_image)
import json

if __name__ == "__main__":
    dbRes = db.fetch_images_url()

    for i in range(len(dbRes)):
        if 'original' in dbRes[i]['images'] and 'manipulated' in dbRes[i]['images']:
            realImg = download_image(dbRes[i]["images"]["original"])
            fakeImage = download_image(dbRes[i]["images"]["manipulated"])
            if realImg is not None and fakeImage is not None and realImg.any() and fakeImage.any():
                realImageDims = merge_images_with_padding(image1=realImg, image2=fakeImage, output_path=rf"C:\Users\User\.vscode\merge_images\images\{i}.png")
                db.save_real_img_dim(id=dbRes[i]['id'], dims=realImageDims)
                # extract_fake_image(merged_image_path=rf"C:\Users\User\.vscode\merge_images\images\{i}.png",fake_image_height=realImageDims["height"],fake_image_width=realImageDims["width"])
