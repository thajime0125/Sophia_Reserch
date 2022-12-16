import os

import pandas as pd
import numpy as np
import cv2

from telop_recognition.utils import telop_recognition
from define_highlight.utils import define_highlight, indexing_frame
from preprocessing.trim_video import trim_video, concat_movie

FILE_DIR = "data/scores/"
MOVIE_FILE = "data/kochi_gameonly.mp4"
TELOP_POSITION = {
    "x": 955,
    "y": 5,
    "width": 320,
    "height": 90
}
SAMPLE_TELOP_FILE = "data/score.jpg"
TELOP_INFO_FILE = "data/telop_info.csv"
MAX_VIDEO_TIME = 2 * 60
DST_FILENAME = "data/highlight.mp4"
SHOT_LIST_PATH = "data/shot_list.csv"


def find_max_below_threshold(numbers, threshold):
    sorted_numbers = sorted(numbers)
    # reversed_numbers = sorted_numbers[::-1]
    max_value = 0
    for value in sorted_numbers:
        if value > threshold:
            break
        max_value = value
    return max_value, value


def main():
    # telop_info = telop_recognition(MOVIE_FILE)
    # telop_info.to_csv(TELOP_INFO_FILE, index=False)
    telop_info = pd.read_csv(TELOP_INFO_FILE)
    telop_info = indexing_frame(telop_info)
    highlight_frame = define_highlight(telop_info)
    shot_list = pd.read_csv(SHOT_LIST_PATH, header=None)[0].to_list()

    # make clips
    clips = []
    clip_frames = []
    total_time = 0
    for index, row in highlight_frame.iterrows():
        print(total_time)
        if total_time > MAX_VIDEO_TIME:
            break
        frame, next_frame = find_max_below_threshold(shot_list, row.frame)
        # clips.append(trim_video(MOVIE_FILE, frame, next_frame))
        # clip_frames.append(frame)
        # total_time += (next_frame - frame) / 30
        if row.point >= 10: # end of game
            clips.append(trim_video(MOVIE_FILE, frame, frame+450))
            clip_frames.append(frame)
            total_time += 15
        elif row.point >= 4: # homerun
            clips.append(trim_video(MOVIE_FILE, frame, frame+600))
            clip_frames.append(frame)
            total_time += 20
        else: # other
            clips.append(trim_video(MOVIE_FILE, frame, frame+450))
            clip_frames.append(frame)
            total_time += 15
    clip_frame_index = np.argsort(clip_frames)
    sort_clips = [clips[i] for i in clip_frame_index]
    concat_movie(sort_clips, DST_FILENAME)

if __name__ == '__main__':
    main()
