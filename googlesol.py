import io
from base64 import b64encode

import os
import cv2
import time
import copy
import torch
import argparse
import threading
import torchvision
import numpy as np
import pandas as pd
import torch.nn as nn

# from moviepy.editor import *
import albumentations as A
from collections import deque

# from google.colab.patches import cv2_imshow
# from google.colab.patches import cv2_imshow

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
CLASSES_LIST = ["fight", "normal"]
SEQUENCE_LENGTH = 16
predicted_class_name = ""


def transform_():
    transform = A.Compose(
        [
            A.Resize(128, 171, always_apply=True),
            A.CenterCrop(112, 112, always_apply=True),
            A.Normalize(
                mean=[0.43216, 0.394666, 0.37645],
                std=[0.22803, 0.22145, 0.216989],
                always_apply=True,
            ),
        ]
    )
    return transform


def loadModel(modelPath):
    PATH = modelPath
    model_ft = torchvision.models.video.mc3_18(weights=True, progress=False)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = torch.nn.Linear(num_ftrs, 2)
    model_ft.load_state_dict(torch.load(PATH, map_location=torch.device(device)))
    model_ft.to(device)
    model_ft.eval()
    return model_ft


def PredTopKClass(k, clips, model):
    with torch.no_grad():

        input_frames = np.array(clips)

        input_frames = np.expand_dims(input_frames, axis=0)

        input_frames = np.transpose(input_frames, (0, 4, 1, 2, 3))

        input_frames = torch.tensor(input_frames, dtype=torch.float32)
        input_frames = input_frames.to(device)

        outputs = model(input_frames)

        soft_max = torch.nn.Softmax(dim=1)
        probs = soft_max(outputs.data)
        prob, indices = torch.topk(probs, k)

    Top_k = indices[0]
    Classes_nameTop_k = [CLASSES_LIST[item].strip() for item in Top_k]
    ProbTop_k = prob[0].tolist()

    ProbTop_k = [round(elem, 5) for elem in ProbTop_k]
    return Classes_nameTop_k[0], probs


def PredTopKProb(k, clips, model):
    with torch.no_grad():
        input_frames = np.array(clips)

        input_frames = np.expand_dims(input_frames, axis=0)

        input_frames = np.transpose(input_frames, (0, 4, 1, 2, 3))

        input_frames = torch.tensor(input_frames, dtype=torch.float32)
        input_frames = input_frames.to(device)

        outputs = model(input_frames)

        soft_max = torch.nn.Softmax(dim=1)
        probs = soft_max(outputs.data)
        # print(probs)
        prob, indices = torch.topk(probs, k)

    Top_k = indices[0]
    Classes_nameTop_k = [CLASSES_LIST[item].strip() for item in Top_k]
    ProbTop_k = prob[0].tolist()
    ProbTop_k = [round(elem, 5) for elem in ProbTop_k]
    return list(zip(Classes_nameTop_k, ProbTop_k))


def predict_on_video(
    video_file_path, output_file_path, model, SEQUENCE_LENGTH, skip=2, showInfo=False
):

    video_reader = cv2.VideoCapture(video_file_path)

    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
    #                                video_reader.get(cv2.CAP_PROP_FPS), (original_video_width, original_video_height))

    frames_queue = deque(maxlen=SEQUENCE_LENGTH)
    transform = transform_()
    predicted_class_name = ""

    counter = 0
    returning_list = []
    while video_reader.isOpened():

        ok, frame = video_reader.read()

        # Check if frame is not read properly then break the loop.
        if not ok:
            break

        image = frame.copy()
        framee = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        framee = transform(image=framee)["image"]
        if counter % skip == 0:
            frames_queue.append(framee)

        if len(frames_queue) == SEQUENCE_LENGTH:
            predicted_class_name, tensor_list = PredTopKClass(1, frames_queue, model)
            returning_list = tensor_list.tolist()
            if showInfo:
                print(predicted_class_name)
                frames_queue = deque(maxlen=SEQUENCE_LENGTH)
            else:
                frames_queue = deque(maxlen=SEQUENCE_LENGTH)

        # if predicted_class_name=="fight":
        #   cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        # else:
        #   print(predicted_class_name['normal'])
        #   cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        counter += 1

        # video_writer.write(frame)
        # time.sleep(2)
        # print(tensor_list)
    if showInfo:
        print(counter)
    video_reader.release()
    # print(tensor_list)
    # return tensor_list
    # video_writer.release()
    return returning_list


torch.backends.cudnn.benchmark = True


class ColabArgs:
    def __init__(
        self,
        model_path,
        streaming,
        input_path,
        output_path,
        sequence_length,
        skip,
        show_info,
    ):
        self.modelPath = model_path
        self.streaming = streaming
        self.inputPath = input_path
        self.outputPath = output_path
        self.sequenceLength = sequence_length
        self.skip = skip
        self.showInfo = show_info


# args = ColabArgs(
#     model_path='models/model_16_m3_0.8888.pth',
#     streaming=False,
#     input_path='video/demo4.avi',
#     output_path='bin/sample.mp4',
#     sequence_length=16,
#     skip=20,
#     show_info=True
# )


def main(args):
    model = loadModel(args.modelPath)

    start = time.time()
    a = predict_on_video(
        args.inputPath,
        args.outputPath,
        model,
        args.sequenceLength,
        args.skip,
        args.showInfo,
    )
    end = time.time()
    return a


# main(args)
