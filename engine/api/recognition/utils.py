import os
import base64
from datetime import datetime
from api import UPLOAD_FOLDER

def current_milli_time():
    return datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")

def b64_to_video(imgstring):
    replace_imgstring = imgstring.replace('data:video/mp4;base64,', '')
    imgdata = base64.b64decode(replace_imgstring, ' /')
    filename = f'video_{current_milli_time()}.mp4'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(file_path, 'wb+') as f:
        f.write(imgdata)
    return filename
