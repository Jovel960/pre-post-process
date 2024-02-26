### **setup & run:**

Our annotation tool: https://sparkling-raindrop-d0ce2b.netlify.app/

1. make sure python is installed
2. clone or fork this repository branch `git clone "https://github.com/Jovel960/pre-post-process.git" then change dir to the project
3. Create a virtual environment in the user's root directory: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` (for MacOS, Unix, or Linux users) or ` .\venv\Scripts\activate` (for Windows users)
5. Install requirements: `pip install -r requirements.txt`\
6. apply `set ENVIRONMENT=envname` options for environments `pre_process|visualize|post_process`
7. run `python main.py`
   8.if you have few merged images (adter running `env_var=pre_process python main.py') -> mark the fake part of the images with our annotation tool -> save the json files inside "json_annotation_files" dir. and if you want to
   visualize the the fake image stand alone then run "visualize" env var.
