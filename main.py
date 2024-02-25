from pre_processing import (merge_images)
from tests import (visualize_annotation_test)
import os

if __name__ == "__main__":
    #bash: env_var="merge_images" python main.py
    #windows: set env_var="merge_images" python main.py
    process_operation = os.getenv('env_var', None)
    if process_operation is not None:
        if process_operation == "merge_images":
            merge_images()  
    else:
        print("Define variable operation on your CLI before running main script!")