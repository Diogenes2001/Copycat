import urllib.request
import tempfile
import cv2
import numpy as np
from posenet.findpose import pose
from backend.verify_action import verify_actions
import re
from zipfile import ZipFile
import json
import os

FPS = 25
TAKE_FRAME_EVERY_N_SECONDS = 0.2
class Game():

    def __init__(self):
        self.past_actions = []

    
    def process_video(self, url):
        print(url)
        if re.search(r'\.mp4', url) is not None:
            temp_video = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.mp4', delete=False)
            video_name = temp_video.name
            urllib.request.urlretrieve(url, video_name) 
        elif re.search(r'\.zip', url) is not None:
            temp_zip = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.zip', delete=False)
            urllib.request.urlretrieve(url, temp_zip.name) 
            temp_dir = tempfile.TemporaryDirectory(delete=False)
            with ZipFile(temp_zip.name, 'r') as zip_ref:
                zip_ref.extractall(temp_dir.name)
            for file in os.listdir(temp_dir.name):
                if file.endswith(".json"):
                    json_path = os.path.join(temp_dir.name, file)
            with open(json_path) as f:
                data = json.load(f)
            # todo: some other way to get video of correct user?
            video_name = os.path.join(temp_dir.name, data['files'][0]['filename'])
            
        elif re.search(r'\.webm', url) is not None:
            # there have been issues with webm with cv2
            temp_video = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.webm', delete=False)
            video_name = temp_video.name
            urllib.request.urlretrieve(url, video_name) 
        else:
            raise "Invalid file format"

        vidcap = cv2.VideoCapture(video_name)
        success,image = vidcap.read()
        count = 0
        seq = []
        take_nth_frame = round(FPS * TAKE_FRAME_EVERY_N_SECONDS)
        while success:
            count += 1
            if count % take_nth_frame == 0:
                print('Saving frame', count)
                temp_image = tempfile.NamedTemporaryFile(prefix='my_image', suffix='.jpg', delete=False)
                cv2.imwrite(temp_image.name, image)     # save frame as JPEG file 
                seq.append(pose(temp_image.name))     
            success,image = vidcap.read()
        
        action_success, new_action = verify_actions(past_actions=self.past_actions, seq=np.array(seq))
        print(new_action)
        if action_success:
            self.past_actions.append(new_action)
        return action_success



# g = Game()
# g.process_video('http://dl5.webmfiles.org/big-buck-bunny_trailer.webm')
# g.process_video('https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4')