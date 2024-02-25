from pre_processing import (merge_images)
from tests import (visualize_annotations)
from post_process import (load_json_files_save_annotation)
import os

if __name__ == "__main__":
    #bash: env_var="merge_images" python main.py
    #windows: set env_var="merge_images" python main.py
    process_operation = os.getenv('env_var', None)
    if process_operation is not None:
        if process_operation == "pre_process":
            merge_images()  
        elif process_operation == "post_process":
            load_json_files_save_annotation()
        elif process_operation == "visualize":
            visualize_annotations()
    else:
        print("Define variable operation on your CLI before running main script!")

