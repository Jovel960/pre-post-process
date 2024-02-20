import db
from merge_images import (merge_images_with_padding, download_image)
import json

if __name__ == "__main__":
    dbRes = db.fetch_images_url()
    print(dbRes)
    # im1 = download_image("https://dailycaller.com/wp-content/uploads/2023/12/Screenshot-2023-12-18-at-9.45.29%E2%80%AFAM-620x329.png")
    # im2 = download_image("https://dailycaller.com/wp-content/uploads/2023/12/Screenshot-2023-12-18-at-9.45.29%E2%80%AFAM-620x329.png")
    # merge_images_with_padding(image1=im1, image2=im2, output_path="combined_image.jpg")
