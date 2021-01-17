import numpy as np
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import cv2 as cv
import math
import tflite_runtime.interpreter as tflite

def initialize():
    # load tflite posenet file and allocate tensors
    mod_path = "posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite"

    interpreter = tflite.Interpreter(model_path=mod_path)
    interpreter.allocate_tensors()

    # get input and output tensors from model
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    return width, height, input_details, output_details, interpreter

def edit_img(width, height, img_path, input_details):
    # resizing image
    img_src = cv.imread(img_path)
    img = cv.resize(img_src, (width, height))
    # add a new dimension to match model's input
    img_input = np.expand_dims(img.copy(), axis=0)

    # check the type of the input tensor
    floating_model = input_details[0]['dtype'] == np.float32
    if floating_model:
        img_input = (np.float32(img_input) - 127.5) / 127.5
    return img_input

def process_images(interpreter, given_input, input_details, output_details):
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

def parse_output(heatmap_data,offset_data, threshold):
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

def interpret_data(img_input, img_heatmap, img_offset, show):
    img_show = np.squeeze((img_input.copy()*127.5+127.5)/255.0)
    img_show = np.array(img_show*255,np.uint8)
    img_kps = parse_output(img_heatmap,img_offset,0.3)
    cv.imshow("image", draw_kps(img_show.copy(),img_kps))
    if show:
        cv.waitKey()
    return img_kps, img_show

def pose(img_path):
    width, height, input_details, output_details, interpreter = initialize()
    img_input = edit_img(width, height, img_path, input_details)
    img_heatmap, img_offset = process_images(interpreter, img_input, input_details, output_details)
    img_kps, img_show = interpret_data(img_input, img_heatmap, img_offset, True)
    return img_kps, img_show

# def run_pose():
#     test3_kps = pose("test3.png")
#     test4_kps = pose("test4.jpeg")
#     print (test3_kps)
#     return test3_kps, test4_kps
# run_pose()
