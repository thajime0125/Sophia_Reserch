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
VIDEO_FPS = 60


def find_max_below_threshold(numbers, threshold, fps):
    sorted_numbers = sorted(numbers)
    # reversed_numbers = sorted_numbers[::-1]
    max_value = 0
    for value in sorted_numbers:
        if value > threshold:
            break
        max_value = value
    if max_value < threshold-15*fps:
        max_value = threshold-15*fps
    return max_value, value


def mov_to_telop_info_csv(movie_path, csv_path, telop_position_ver=1):
    telop_info = telop_recognition(movie_path, telop_position_ver=telop_position_ver)
    telop_info.to_csv(csv_path, index=False)


def use_shot(movie_file, telop_info_file, shot_list_path, max_video_time, dst_filename, video_fps):
    # make telop_info.csv
    # mov_to_telop_info_csv(movie_file, telop_info_file)

    telop_info = pd.read_csv(telop_info_file)
    telop_info = indexing_frame(telop_info)
    highlight_frame = define_highlight(telop_info)
    shot_list = pd.read_csv(shot_list_path, header=None)[0].to_list()

    # make clips
    clips = []
    clip_frames = []
    total_time = 0
    for index, row in highlight_frame.iterrows():
        print(total_time)
        if total_time > max_video_time:
            break
        frame, next_frame = find_max_below_threshold(shot_list, row.frame, video_fps)
        # clips.append(trim_video(MOVIE_FILE, frame, next_frame))
        # clip_frames.append(frame)
        # total_time += (next_frame - frame) / 30
        if row.point >= 10: # end of game
            clips.append(trim_video(movie_file, frame, 15, video_fps))
            clip_frames.append(frame)
            total_time += 15
        elif row.point >= 4: # homerun
            clips.append(trim_video(movie_file, frame, 20, video_fps))
            clip_frames.append(frame)
            total_time += 20
        else: # other
            clips.append(trim_video(movie_file, frame, 15, video_fps))
            clip_frames.append(frame)
            total_time += 15
    clip_frame_index = np.argsort(clip_frames)
    sort_clips = [clips[i] for i in clip_frame_index]
    concat_movie(sort_clips, dst_filename)


def nonuse_shot(movie_file, telop_info_file, max_video_time, dst_filename, video_fps):
    # make telop_info.csv
    # mov_to_telop_info_csv(movie_file, telop_info_file)

    telop_info = pd.read_csv(telop_info_file)
    telop_info = indexing_frame(telop_info)
    highlight_frame = define_highlight(telop_info)

    # make clips
    clips = []
    clip_frames = []
    total_time = 0
    for index, row in highlight_frame.iterrows():
        print(total_time)
        if total_time > max_video_time:
            break
        frame = row.frame
        # clips.append(trim_video(MOVIE_FILE, frame, next_frame))
        # clip_frames.append(frame)
        # total_time += (next_frame - frame) / 30
        if row.point >= 10: # end of game
            clips.append(trim_video(movie_file, frame-10*video_fps, 15, video_fps))
            clip_frames.append(frame)
            total_time += 15
        elif row.point >= 4: # homerun
            clips.append(trim_video(movie_file, frame-10*video_fps, 20, video_fps))
            clip_frames.append(frame)
            total_time += 20
        else: # other
            clips.append(trim_video(movie_file, frame-10*video_fps, 15, video_fps))
            clip_frames.append(frame)
            total_time += 15
    clip_frame_index = np.argsort(clip_frames)
    sort_clips = [clips[i] for i in clip_frame_index]
    concat_movie(sort_clips, dst_filename)


if __name__ == '__main__':
    # mov_to_telop_info_csv('data/highlight_test_movie/0416.mp4', 'data/highlight_test_movie/0416.csv', 2)
    use_shot(
        'data/highlight_test_movie/0416.mp4', 
        'data/highlight_test_movie/0416.csv', 
        SHOT_LIST_PATH,
        2*60, 
        'data/highlight_test_movie/416_highlight.mp4',
        VIDEO_FPS
    )
