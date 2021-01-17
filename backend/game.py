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
from moviepy.video.io.VideoFileClip import VideoFileClip

MIN_SCORE = 70
class Game():

    def __init__(self):
        self.last_path = ""
        # need this to stop temp files from closing
        self.last_temp_thing = None

    
    def process_video(self, url, filename):
        print(url)
        if re.search(r'\.mp4', url) is not None:
            temp_thing = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.mp4', delete=False)
            video_name = temp_thing.name
            urllib.request.urlretrieve(url, video_name) 
        elif re.search(r'\.zip', url) is not None:
            temp_zip = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.zip', delete=False)
            urllib.request.urlretrieve(url, temp_zip.name) 
            temp_thing = tempfile.TemporaryDirectory()
            with ZipFile(temp_zip.name, 'r') as zip_ref:
                zip_ref.extractall(temp_thing.name)
            for file in os.listdir(temp_thing.name):
                if file.endswith(".json"):
                    json_path = os.path.join(temp_thing.name, file)
            with open(json_path) as f:
                data = json.load(f)
            # use the filename passed as an argument
            video_name = os.path.join(temp_thing.name, filename)
            
            
        elif re.search(r'\.webm', url) is not None:
            # there have been issues with webm with cv2
            temp_thing = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.webm', delete=False)
            video_name = temp_thing.name
            urllib.request.urlretrieve(url, video_name) 
        else:
            raise "Invalid file format"

        if self.last_path != "":
            trimmed_video = tempfile.NamedTemporaryFile(prefix='trimmed', suffix='.webm', delete=False)
            with VideoFileClip(video_name) as video:
                new = video.subclip(0, video.duration - 5)
                new.write_videofile(trimmed_video.name, audio_codec='aac')
            temp_pickle = tempfile.NamedTemporaryFile(prefix='lookup', suffix='.pickle', delete=False)
            os.system('py posenet/keypoints_from_video.py --activity "stuff" --video "' + \
                 self.last_path + \
                     '" --lookup "' + temp_pickle.name + '"')
            os.system('py posenet/start_here.py --activity "stuff" --video "' + \
                 trimmed_video.name + \
                     '" --lookup "' + temp_pickle.name + '"')
            f = open("out.txt", "r")
            score = float(f.read())
            if score < MIN_SCORE:
                return False
        self.last_path = video_name
        self.last_temp_thing = temp_thing 
        return True
        # vidcap = cv2.VideoCapture(video_name)
        # success,image = vidcap.read()
        # count = 0
        # seq = []
        # take_nth_frame = round(FPS * TAKE_FRAME_EVERY_N_SECONDS)
        # while success:
        #     count += 1
        #     if count % take_nth_frame == 0:
        #         print('Saving frame', count)
        #         temp_image = tempfile.NamedTemporaryFile(prefix='my_image', suffix='.jpg', delete=False)
        #         cv2.imwrite(temp_image.name, image)     # save frame as JPEG file 
        #         seq.append(pose(temp_image.name))     
        #     success,image = vidcap.read()
        
        # action_success, new_action = verify_actions(past_actions=self.past_actions, seq=np.array(seq))
        # print(new_action)
        # if action_success:
        #     self.past_actions.append(new_action)
        # return action_success


# g = Game()
# g.process_video('http://dl5.webmfiles.org/big-buck-bunny_trailer.webm')
# g.process_video('https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4')