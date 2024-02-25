import os
from merge_images import (adjust_annotation_for_fake_image_with_all_padding)
import json
import db
json_folder_path = "json_annotatios_files"


def load_json_files_save_annotation():
    listDir = os.listdir(json_folder_path)
    if len(listDir):
        for filename in listDir(json_folder_path):
            if filename.endswith(".json"):
                with open(os.path.join(json_folder_path, filename), "r", encoding='utf-8') as file:
                    data = json.loads(file.read())
                    # Split the string on the last dot (from the right), splitting only once
                    parts = data["images"][0]["file_name"].rsplit('.', 1)
                    # Rejoin all parts except the last one (the file extension)
                    text = parts[0] if len(parts) > 1 else filename
                    db.save_adjusted_annotation(text = text,annotation={"annotations":data["annotations"][0]["segmentation"], "bbox":data["annotations"][0]["bbox"]})
    else:
        print("json files dir is empty!")