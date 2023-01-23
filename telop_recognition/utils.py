import os

import pandas as pd
import cv2

from telop_recognition.telop_reading import *

FILE_DIR = "data/scores/"
MOVIE_FILE = "data/kochi_gameonly.mp4"
TELOP_POSITION = {
    "x": 955,
    "y": 5,
    "width": 320,
    "height": 90
}
TELOP_POSITION_VER2 = {
    "x": 980,
    "y": 5,
    "width": 295,
    "height": 85
}
SAMPLE_TELOP_FILE = "data/score.jpg"


def telop_recognition(movie_file, telop_position_ver=1):
    # Read movie file
    movie = cv2.VideoCapture(movie_file)
    telop_tar = cv2.imread(SAMPLE_TELOP_FILE)
    telop_info = []
    total_frame = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    telop_position = TELOP_POSITION if telop_position_ver == 1 else TELOP_POSITION_VER2
    i = 0
    while True:
        try:
            ret, frame = movie.read()
            if i % 30 == 0:
                telop = frame[
                    telop_position["y"]:telop_position["y"] + telop_position["height"],
                    telop_position["x"]:telop_position["x"] + telop_position["width"]
                ]
                telop = cv2.resize(telop, (telop_tar.shape[1], telop_tar.shape[0]))
                telop_diff = cv2.absdiff(telop, telop_tar)
                # print(telop_diff.mean())
                if telop_diff.mean() < 35:
                    count = reading_count(telop)
                    base = reading_base(telop)
                    # score = reading_score(telop)
                    inning = reading_inning(telop)
                    telop_info.append([i, inning, base, count, "[0, 0]"])
        except:
            pass

        i += 1
        if i == total_frame:
            break
        if i % 1000 == 0:
            print(i)

    telop_info = pd.DataFrame(
        telop_info, columns=["frame", "inning", "base", "count", "score"])

    return telop_info

