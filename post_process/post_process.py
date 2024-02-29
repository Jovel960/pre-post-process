import os
from merge_images import (adjust_annotation_for_images)
import json
import db
json_folder_path = "json_annotatios_files"


def load_json_files_save_annotation():
    listDir = os.listdir(json_folder_path)
    if len(listDir):
        for filename in listDir:
            if filename.endswith(".json"):
                with open(os.path.join(json_folder_path, filename), "r", encoding='utf-8') as file:
                    data = json.loads(file.read())
                    # Split the string on the last dot (from the right), splitting only once
                    parts = data["images"][0]["file_name"].rsplit('.', 1)
                    # Rejoin all parts except the last one (the file extension)
                    id = parts[0] if len(parts) > 1 else filename
                    dims = json.loads(db.fetch_dims(id.strip())[0])
                    adjusted_annotation = adjust_annotation_for_images(original_image_padded=dims["is_real_image_padded"],
                                                                       original_width=dims["real_image_width"],
                                                                    bottom_padding=dims["pad_bottom"],
                                                                    fake_height=dims["fake_image_height"],
                                                                    fake_width=dims["fake_image_width"],
                                                                    left_padding=dims["pad_left"],
                                                                    merged_height=dims["combined_image_height"],
                                                                    merged_width=dims["combined_image_width"],
                                                                    right_padding=dims["pad_right"],
                                                                    top_padding=dims["pad_top"],
                                                                    segmentation=data["annotations"][0]["segmentation"], 
                                                                    bbox=data["annotations"][0]["bbox"]
                                                        )
                    db.save_adjusted_annotation(id = id,annotation={"annotations":adjusted_annotation[0], "bbox":adjusted_annotation[1]})
    else:
        print("json files dir is empty!")