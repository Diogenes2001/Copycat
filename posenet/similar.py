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

def draw_deviations(img, keypoints, pairs, deviations):

    for i, pair in enumerate(pairs):
        if i in deviations:
            color = (0,0,255)
        else:
            color = (0,255,0)
        cv.line(img, (keypoints[pair[0]][1], keypoints[pair[0]][0]), (keypoints[pair[1]][1], keypoints[pair[1]][0]), color=color, lineType=cv.LINE_AA, thickness=1)

# connect some of the points 
def join_point(img, kps):
    body_parts = [(5,6),(5,7),(6,8),(7,9),(8,10),(11,12),(5,11),
                        (6,12),(11,13),(12,14),(13,15),(14,16)]

    for part in body_parts:
        cv.line(img, (kps[part[0]][1], kps[part[0]][0]), (kps[part[1]][1], kps[part[1]][0]), 
                color=(255,255,255), lineType=cv.LINE_AA, thickness=3)

def draw_skeleton(img_show, img_kps):
    # Get a zero matrix with the shape of the image
    img_pose = np.zeros_like(img_show)

    # draw a skeleton of the pose to the empty image
    join_point(img_pose, img_kps[:, :2])
    # set the new dimensions of the image to reduce the size
    # buffer = 25 # size of the area around the pose
    # top_left_y = min(img_kps[5:, 0]) - buffer
    # top_left_x = min(img_kps[5:, 1]) - buffer
    # buttom_right_y = max(img_kps[5:, 0]) + buffer
    # buttom_right_x = max(img_kps[5:, 1]) + buffer

    # # crop the pose with new dimensions
    # img_pose = img_pose[top_left_y:buttom_right_y, top_left_x:buttom_right_x]
    img_pose = cv.cvtColor(img_pose, cv.COLOR_BGR2GRAY)
    return img_pose

def findDeviations():
    original_kps, original_show = pose("test8.jpg")
    new_kps, new_show = pose("test9.jpg")

    original_values = generate_values(original_kps)
    new_values = generate_values(new_kps)
    deviations = matching(original_values, new_values)

    draw_deviations(new_show, new_kps, connected_points, deviations)
    cv.imshow("deviations", new_show)
    cv.waitKey()

    # original_pose = draw_skeleton(original_show, original_kps)
    # new_pose = draw_skeleton(new_show, new_kps)
    # cv.imshow("pose1", original_pose)
    # cv.imshow("pose2", new_pose)
    # cv.waitKey()

    # # the greater the threshold the more exact the pose has to match
    # threshold = 0.1

    # w, h = new_pose.shape[::-1]
    # res = cv.matchTemplate(new_pose,original_pose, cv.TM_CCOEFF_NORMED)
    # score = res.max()
    # print("score:", score)

    # if score >= threshold:
    #     print("Match")
    # else:
    #     print("Don't match")

    # return deviations, original_show

# deviations, original_show = findDeviations()
findDeviations()