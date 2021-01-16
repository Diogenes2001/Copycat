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

data1_kps = pose("test5.png")
data2_kps = pose("test4.jpeg")

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

print (original_values)