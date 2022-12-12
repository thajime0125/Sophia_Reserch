import os
import re

import cv2
import pytesseract
import pyocr
from PIL import Image

filedir = "data/scores/"


def is_positive_count(img, color_type):
    img_tar = img[:, :, color_type]
    if img_tar.mean() > 50 and img_tar.mean() < 80:
        return 0
    else:
        return 1


def is_positive_base(img):
    if img.mean() < 50:
        return 0
    else:
        return 1


def number_recognition(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pil_image = Image.fromarray(img_gray)
    tools = pyocr.get_available_tools()
    tool = tools[0]
    builder = pyocr.builders.TextBuilder(tesseract_layout=10)
    num = tool.image_to_string(pil_image, builder=builder)
    num = re.sub(r"[^0-9]", "", num)
    return int(num)


def reading_count(img):

    # reading ball_count
    ball_1 = img[48:57, 211:220]
    if is_positive_count(ball_1, 0):
        ball_2 = img[48:57, 225:234]
        if is_positive_count(ball_2, 0):
            ball_3 = img[48:57, 238:247]
            if is_positive_count(ball_3, 0):
                ball_count = 3
            else:
                ball_count = 2
        else:
            ball_count = 1
    else:
        ball_count = 0

    # reading strike_count
    strike_1 = img[63:72, 211:220]
    if is_positive_count(strike_1, 2):
        strike_2 = img[63:72, 224:233]
        if is_positive_count(strike_2, 2):
                strike_count = 2
        else:
            strike_count = 1
    else:
        strike_count = 0

    # reading out_count
    out_1 = img[78:87, 212:221]
    if is_positive_count(out_1, 2):
        out_2 = img[78:87, 224:233]
        if is_positive_count(out_2, 2):
                out_count = 2
        else:
            out_count = 1
    else:
        out_count = 0
    
    return [ball_count, strike_count, out_count]


def reading_base(img):

    # define initial base
    base = [0, 0, 0]

    # reading 1st_base
    base_1 = img[54:61, 309:316]
    if is_positive_base(base_1):
        base[0] = 1
    # reading 2nd_base
    base_2 = img[27:34, 283:290]
    if is_positive_base(base_2):
        base[1] = 1
    # reading 3rd_base
    base_3 = img[54:61, 256:263]
    if is_positive_base(base_3):
        base[2] = 1

    return base


def reading_score(img):

    score_1_img = img[42:68, 168:189]
    score_1 = number_recognition(score_1_img)
    score_2_img = img[70:, 168:189]
    score_2 = number_recognition(score_2_img)

    return [score_1, score_2]


def reading_inning(img):
    inning_num = number_recognition(img[48:74, 272:288])
    return inning_num


if __name__ == '__main__':
    n = 78900
    filepath = f'{filedir}score{n}.jpg'
    img = cv2.imread(filepath)
    
    count = reading_count(img)
    base = reading_base(img)
    score = reading_score(img)
    inning = reading_inning(img)

    print(f'count: {count}\nbase: {base}\nscore: {score}\ninning: {inning}')

