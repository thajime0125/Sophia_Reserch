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
SAMPLE_TELOP_FILE = "data/score.jpg"


def telop_recognition():
    # Read movie file
    movie = cv2.VideoCapture(MOVIE_FILE)
    telop_tar = cv2.imread(SAMPLE_TELOP_FILE)
    telop_info = []
    total_frame = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    while True:
        try:
            ret, frame = movie.read()
            if i % 30 == 0:
                telop = frame[
                    TELOP_POSITION["y"]:TELOP_POSITION["y"] + TELOP_POSITION["height"], 
                    TELOP_POSITION["x"]:TELOP_POSITION["x"] + TELOP_POSITION["width"]
                    ]
                telop_diff = cv2.absdiff(telop, telop_tar)
                if telop_diff.mean() < 30:
                    count = reading_count(telop)
                    base = reading_base(telop)
                    score = reading_score(telop)
                    inning = reading_inning(telop)
                    telop_info.append([i, inning, base, count, score])
        except:
            pass
                
        i += 1
        if i == total_frame:
                break
        if i % 1000 == 0:
            print(i)

    telop_info = pd.DataFrame(telop_info, columns=["frame", "inning", "base", "count", "score"])

    return telop_info


# def highlight_detection(telop_info):


def main():
    telop_info = telop_recognition()
    telop_info.to_csv("data/telop_info.csv", index=False)

if __name__ == '__main__':
    main()
