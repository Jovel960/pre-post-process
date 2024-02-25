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



