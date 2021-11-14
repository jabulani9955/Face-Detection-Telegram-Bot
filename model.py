import os
import subprocess
import cv2
import matplotlib.pyplot as plt


def get_predict(img_path):
    PH = "/home/jabulani/Bot_Faces/darknet/"
    os.system(f"{PH}darknet detector test /home/jabulani/Bot_Faces/darknet/cfg/coco.data {PH}cfg/custom-yolov4-tiny-detector.cfg /home/jabulani/Bot_Faces/darknet/backup/custom-yolov4-tiny-detector_best_2.weights {img_path} -thresh 0.7 -dont-show -ext-output <darknet/data/train.txt> result.txt")
    with open(f'result.txt') as f:
        text = f.read().split('\n')
        text = list(filter(None, text))
        out = text[8:]
    return ('\n'.join(out), f'predictions.jpg') if out else ('Не могу никого узнать :(', f'predictions.jpg')

