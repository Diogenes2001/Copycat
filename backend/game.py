import urllib.request
import tempfile
import cv2
import numpy as np
from posenet.findpose import pose
from backend.verify_action import verify_actions

FPS = 25
TAKE_FRAME_EVERY_N_SECONDS = 0.2
class Game():

    def __init__(self):
        self.past_actions = []

    
    def process_video(self, url):
        temp_video = tempfile.NamedTemporaryFile(prefix='my_video', suffix='.mp4', delete=False)
        urllib.request.urlretrieve(url, temp_video.name) 
        vidcap = cv2.VideoCapture(temp_video.name)
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
        if action_success:
            self.past_actions.append(new_action)
        return action_success



# g = Game()
# g.process_video('https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4')
# g.process_video('https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4')