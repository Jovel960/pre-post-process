import db.sqlite as sqlite
from merge_images import (merge_images_with_padding, download_image)
import json

if __name__ == "__main__":
    sqlite.connectToDb()
    dbRes = sqlite.createQuery('select images from trainData where LENGTH(images) > 0;')
    print(json.loads(dbRes[0][0]))
    # im1 = download_image("https://dailycaller.com/wp-content/uploads/2023/12/Screenshot-2023-12-18-at-9.45.29%E2%80%AFAM-620x329.png")
    # im2 = download_image("https://dailycaller.com/wp-content/uploads/2023/12/Screenshot-2023-12-18-at-9.45.29%E2%80%AFAM-620x329.png")
    # merge_images_with_padding(image1=im1, image2=im2, output_path="combined_image.jpg")
