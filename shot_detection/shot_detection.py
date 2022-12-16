import time

import cv2
import numpy as np
import pandas as pd

filepath = "data/kochi_gameonly.mp4" # movie file

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
    template_frame = cv2.imread("data/template.jpg")
    movie_stop_frame = 0
    for i in range(int(total_frame)):
        try:
            frame_before = frame
            ret, frame = movie.read()
            frame_diff = cv2.absdiff(frame_before, frame)
            frame_mean = frame_diff.mean()
            if frame_mean < threshold:
                movie_stop_frame += 1
                if movie_stop_frame == 45:
                    temp_diff = cv2.absdiff(frame, template_frame)
                    if temp_diff.mean() < 60:
                        shot_list.append(i)
                        print(i, temp_diff.mean())
            else:
                movie_stop_frame = 0
        except:
            pass
    
    shot_df = pd.DataFrame(shot_list)
    return shot_df

if __name__ == '__main__':
    movie = read_movie(filepath)
    shot_df = shot_detection(movie, 5)
    print(shot_df)
    shot_df.to_csv("data/shot_list.csv", index=False)
