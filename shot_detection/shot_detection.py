import time

import cv2
import numpy as np
import pandas as pd

# filepath = "../data/kochi_gameonly.mp4" # movie file

def read_movie(filepath):
    movie = cv2.VideoCapture(filepath)
    if not movie.isOpened():
        print("can't open")
        exit()
    return movie


def shot_detection(movie, threshold):
    shot_list = []
    ret, frame = movie.read()
    total_frame = movie.get(cv2.CAP_PROP_FRAME_COUNT)
    for i in range(int(total_frame)):
        frame_before = frame
        ret, frame = movie.read()
        frame_diff = cv2.absdiff(frame_before, frame)
        frame_mean = frame_diff.mean()
        if frame_mean > 40:
            shot_list.append(frame)
    
    shot_df = pd.DataFrame(shot_list)
    return shot_df

