import sklearn as skl
import numpy as np
import math

data =  np.array([[ 27, 123,   1],
       [ 22, 127,   1],
       [ 23, 119,   1],
       [ 25, 134,   1],
       [ 26, 112,   1],
       [ 55, 147,   1],
       [ 53, 103,   1],
       [ 77, 166,   1],
       [ 80,  83,   1],
       [105, 156,   1],
       [107,  90,   1],
       [120, 138,   1],
       [119, 113,   1],
       [172, 126,   1],
       [173, 129,   1],
       [225, 143,   1],
       [225, 102,   1]])

def keypoints_to_vector(keypoints):
    out = []
    for kp in keypoints:
        out.append(kp[0])
        out.append(kp[1])
    return np.array(out)

def dist(v1, v2):
    return math.sqrt(2 * (1-skl.metrics.pairwise.cosine_similarity(v1, v2)))

NUM_FRAMES_SAVED = 4
def extract_action(frames):
    interval = round(frames.shape[0] / (NUM_FRAMES_SAVED + 1))
    indices = [i for i in range(interval, frames.shape[0]-interval, interval)]
    return frames[indices]


MAXIMUM_DISTANCE = 0.2
def verify_actions(past_actions, seq):
    frames = np.array([keypoints_to_vector(kp) for kp in seq])
    for action in past_actions:
        for frame in action:
            dists = [dist(frame, new_frame) for new_frame in frames]
            i = np.argmin(dists)
            if dists[i] > MAXIMUM_DISTANCE:
                return False, None
            frames = frames[i:]
    return True, extract_action(frames)
        
# print(keypoints_to_vector(data))
