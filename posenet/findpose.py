import numpy as np
# import scipy as sp
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import cv2 as cv
import math
import tflite_runtime.interpreter as tflite

# load tflite posenet file and allocate tensors
path = "posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite"
compare_path = "test3.png"
input_path = "test4.jpeg"

interpreter = tflite.Interpreter(model_path=path)
interpreter.allocate_tensors()

# get input and output tensors from model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# resizing images
compare_image_src = cv.imread(compare_path)
compare_image = cv.resize(compare_image_src, (width, height))
# cv.imshow("compare image", compare_image)

input_image_src = cv.imread(input_path)
input_image = cv.resize(input_image_src, (width, height))
# cv.imshow("input image", input_image)

# add a new dimension to match model's input
compare_input = np.expand_dims(compare_image.copy(), axis=0)
input_input = np.expand_dims(input_image.copy(), axis=0)

# check the type of the input tensor
floating_model = input_details[0]['dtype'] == np.float32
if floating_model:
  compare_input = (np.float32(compare_input) - 127.5) / 127.5
  input_input = (np.float32(input_input) - 127.5) / 127.5

# test the model on random input data
# input_shape = input_details[0]['shape']
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# interpreter.set_tensor(input_details[0]['index'], input_data)

# Process images
# Sets the value of the input tensor
# interpreter.set_tensor(input_details[0]['index'], compare_input)
# interpreter.invoke()

# # Extract output data from the interpreter
# compare_output_data = interpreter.get_tensor(output_details[0]['index'])
# compare_offset_data = interpreter.get_tensor(output_details[1]['index'])

# # Getting rid of the extra dimension
# compare_heatmaps = np.squeeze(compare_output_data)
# compare_offsets = np.squeeze(compare_offset_data)
# print("compare_heatmaps' shape:", compare_heatmaps.shape)
# print("compare_offsets' shape:", compare_offsets.shape)

# interpreter.set_tensor(input_details[0]['index'], input_input)
# interpreter.invoke()
# input_output_data = interpreter.get_tensor(output_details[0]['index'])
# input_offset_data = interpreter.get_tensor(output_details[1]['index'])
# input_heatmaps = np.squeeze(input_output_data)
# input_offsets = np.squeeze(input_offset_data)



def process_images(interpreter, given_input):
    # Sets the value of the input tensor
    interpreter.set_tensor(input_details[0]['index'], given_input)
    interpreter.invoke()

    # Extract output data from the interpreter
    given_output_data = interpreter.get_tensor(output_details[0]['index'])
    given_offset_data = interpreter.get_tensor(output_details[1]['index'])

    # Getting rid of the extra dimension
    given_heatmaps = np.squeeze(given_output_data)
    given_offsets = np.squeeze(given_offset_data)
    print("heatmaps' shape:", given_heatmaps.shape)
    print("offsets' shape:", given_offsets.shape)

    return given_heatmaps, given_offsets

compare_heatmaps, compare_offsets = process_images(interpreter, compare_input)
input_heatmaps, input_offsets = process_images(interpreter, input_input)


def parse_output(heatmap_data,offset_data, threshold):

    '''
    Input:
        heatmap_data - hetmaps for an image. Three dimension array
        offset_data - offset vectors for an image. Three dimension array
        threshold - probability threshold for the keypoints. Scalar value
    Output:
        array with coordinates of the keypoints and flags for those that have
        low probability
    '''

    joint_num = heatmap_data.shape[-1]
    pose_kps = np.zeros((joint_num,3), np.uint32)

    for i in range(heatmap_data.shape[-1]):

        joint_heatmap = heatmap_data[...,i]
        max_val_pos = np.squeeze(np.argwhere(joint_heatmap==np.max(joint_heatmap)))
        remap_pos = np.array(max_val_pos/8*257,dtype=np.int32)
        pose_kps[i,0] = int(remap_pos[0] + offset_data[max_val_pos[0],max_val_pos[1],i])
        pose_kps[i,1] = int(remap_pos[1] + offset_data[max_val_pos[0],max_val_pos[1],i+joint_num])
        max_prob = np.max(joint_heatmap)

        if max_prob > threshold:
            if pose_kps[i,0] < 257 and pose_kps[i,1] < 257:
                pose_kps[i,2] = 1

    return pose_kps

def draw_kps(show_img,kps, ratio=None):
    for i in range(5,kps.shape[0]):
      if kps[i,2]:
        if isinstance(ratio, tuple):
            cv.circle(show_img,(int(round(kps[i,1]*ratio[1])),int(round(kps[i,0]*ratio[0]))),2,(0,255,0),round(int(1*ratio[1])))
            continue
        cv.circle(show_img,(kps[i,1],kps[i,0]),2,(0,255,0),-1)
    return show_img

compare_show = np.squeeze((compare_input.copy()*127.5+127.5)/255.0)
compare_show = np.array(compare_show*255,np.uint8)
compare_kps = parse_output(compare_heatmaps,compare_offsets,0.3)
cv.imshow("compare image", draw_kps(compare_show.copy(),compare_kps))

input_show = np.squeeze((input_input.copy()*127.5+127.5)/255.0)
input_show = np.array(input_show*255,np.uint8)
input_kps = parse_output(input_heatmaps,input_offsets,0.3)
cv.imshow("input image", draw_kps(input_show.copy(),input_kps))
cv.waitKey()

# extract output data from the interpreter
# output: "probability of appearance of each keypoint in the particular part of the image (9,9)"
# offset: "more exact calculation of the keypoint’s position"
# output_data = interpreter.get_tensor(output_details[0]['index'])
# offset_data = interpreter.get_tensor(output_details[1]['index'])
# print(output_data)