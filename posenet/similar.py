import numpy as np
# import scipy as sp
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import cv2 as cv
import math
import tflite_runtime.interpreter as tflite
from findpose import pose

connected_points = [(5,6),(5,7),(6,8),(7,9),(8,10),(11,12),(5,11),(6,12),(11,13),(12,14),(13,15),(14,16)]

data1_kps, data1_show = pose("test3.png")
data2_kps, data2_show = pose("test4.jpeg")

def angle_length(p1, p2):
    angle = math.atan2(- int(p2[0]) + int(p1[0]), int(p2[1]) - int(p1[1])) * 180.0 / np.pi
    length = math.hypot(int(p2[1]) - int(p1[1]), - int(p2[0]) + int(p1[0]))
    
    return round(angle), round(length)

def generate_values(img_kps):
    img_values = []
    print(img_kps)
    for point in connected_points:
        img_values.append(angle_length(img_kps[point[0]][:2], img_kps[point[1]][:2]))
    return img_values

original_values = generate_values(data1_kps)
new_values = generate_values(data2_kps)

def matching(original_kp, new_kp, angle_deviation=30, size_deviation=1):
    deviation = []
    # set an anchor size for proportions calculations - distance between shoulders
    original_anchor = original_kp[0][1]
    new_anchor = new_kp[0][1]

    # for each body part that we calculated angle and size for
    for i in range(len(original_kp)):

        angles = (original_kp[i][0], new_kp[i][0])
        diff_angle = max(angles) - min(angles)

        original_size = (original_kp[i][1],original_anchor)
        original_size = abs(min(original_size) / max(original_size))

        new_size = (new_kp[i][1], new_anchor)
        new_size = abs(min(new_size) / max(new_size))

        if diff_angle > angle_deviation:
            deviation.append(i)
            print("{0} has different angle".format(i))

        elif max(new_size,original_size) - min(new_size,original_size) > size_deviation:
            deviation.append(i)
            print("{0} has different size".format(i))

    return deviation

deviations = matching(original_values, new_values)
print (deviations)

def draw_deviations(img, keypoints, pairs, deviations):

    for i, pair in enumerate(pairs):

        if i in deviations:
            color = (0,0,255)
        else:
            color = (0,255,0)
        
        cv.line(img, (keypoints[pair[0]][1], keypoints[pair[0]][0]), (keypoints[pair[1]][1], keypoints[pair[1]][0]), color=color, lineType=cv.LINE_AA, thickness=1)

draw_deviations(data2_show, data2_kps, connected_points, deviations)
cv.imshow("deviations", data2_show)
cv.waitKey()