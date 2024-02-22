import os
from merge_images import (adjust_annotation_for_fake_image_with_all_padding)
import json
import db
json_folder_path = "json_annotatios_files"


def load_json_files():
    for filename in os.listdir(json_folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(json_folder_path, filename), "r", encoding='utf-8') as file:
                data = json.loads(file.read())
                return {"annotations":data["annotations"][0]["segmentation"], "bbox":data["annotations"][0]["bbox"]}


if __name__ == "__main__":
    load_json_files()