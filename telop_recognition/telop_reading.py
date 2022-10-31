import os

import pandas as pd
import cv2

filedir = "data/scores/"


def reading_color(img, color_type):
    img_tar = img[:, :, color_type]
    if img_tar.mean() > 50 and img_tar.mean() < 80:
        return 0
    else:
        return 1


def reading_count(img):

    # reading ball_count
    ball_1 = img[48:57, 211:220]
    if reading_color(ball_1, 0):
        ball_2 = img[48:57, 225:234]
        if reading_color(ball_2, 0):
            ball_3 = img[48:57, 238:247]
            if reading_color(ball_3, 0):
                ball_count = 3
            else:
                ball_count = 2
        else:
            ball_count = 1
    else:
        ball_count = 0

    # reading strike_count
    strike_1 = img[63:72, 211:220]
    if reading_color(strike_1, 2):
        strike_2 = img[63:72, 224:233]
        if reading_color(strike_2, 2):
                strike_count = 2
        else:
            strike_count = 1
    else:
        strike_count = 0

    # reading out_count
    out_1 = img[78:87, 212:221]
    if reading_color(out_1, 2):
        out_2 = img[78:87, 224:233]
        if reading_color(out_2, 2):
                out_count = 2
        else:
            out_count = 1
    else:
        out_count = 0
    
    return ball_count, strike_count, out_count

if __name__ == '__main__':
    n = 38400
    filepath = f'{filedir}score{n}.jpg'
    img = cv2.imread(filepath)
    
    b, s, o = reading_count(img)
    print(b, s, o)
