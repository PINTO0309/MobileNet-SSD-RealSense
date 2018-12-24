import sys
import numpy as np
import cv2
from os import system
import io, time
from os.path import isfile, join
import re
from openvino.inference_engine import IENetwork, IEPlugin

fps = ""
detectfps = ""
framecount = 0
detectframecount = 0
time1 = 0
time2 = 0

LABELS = ('background',
          'aeroplane', 'bicycle', 'bird', 'boat',
          'bottle', 'bus', 'car', 'cat', 'chair',
          'cow', 'diningtable', 'dog', 'horse',
          'motorbike', 'person', 'pottedplant',
          'sheep', 'sofa', 'train', 'tvmonitor')

camera_width = 320
camera_height = 240

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

plugin = IEPlugin(device="MYRIAD")
#plugin.set_config({"VPU_FORCE_RESET": "NO"})
net = IENetwork("lrmodel/MobileNetSSD/MobileNetSSD_deploy.xml", "lrmodel/MobileNetSSD/MobileNetSSD_deploy.bin")
input_blob = next(iter(net.inputs))
exec_net = plugin.load(network=net)

try:

    while True:
        t1 = time.perf_counter()

        ret, color_image = cap.read()
        if not ret:
            break

        height = color_image.shape[0]
        width = color_image.shape[1]

        prepimg = cv2.resize(color_image, (300, 300))
        prepimg = prepimg - 127.5
        prepimg = prepimg * 0.007843
        prepimg = prepimg[np.newaxis, :, :, :]
        prepimg = prepimg.transpose((0, 3, 1, 2))  #NHWC to NCHW
        out = exec_net.infer(inputs={input_blob: prepimg})
        out = out["detection_out"].flatten()

        for box_index in range(100):
            if out[box_index + 1] == 0.0:
                break
            base_index = box_index * 7
            if (not np.isfinite(out[base_index]) or
                not np.isfinite(out[base_index + 1]) or
                not np.isfinite(out[base_index + 2]) or
                not np.isfinite(out[base_index + 3]) or
                not np.isfinite(out[base_index + 4]) or
                not np.isfinite(out[base_index + 5]) or
                not np.isfinite(out[base_index + 6])):
                continue

            if box_index == 0:
                detectframecount += 1

            x1 = max(0, int(out[base_index + 3] * height))
            y1 = max(0, int(out[base_index + 4] * width))
            x2 = min(height, int(out[base_index + 5] * height))
            y2 = min(width, int(out[base_index + 6] * width))

            object_info_overlay = out[base_index:base_index + 7]

            min_score_percent = 60
            source_image_width = width
            source_image_height = height

            base_index = 0
            class_id = object_info_overlay[base_index + 1]
            percentage = int(object_info_overlay[base_index + 2] * 100)
            if (percentage <= min_score_percent):
                continue

            box_left = int(object_info_overlay[base_index + 3] * source_image_width)
            box_top = int(object_info_overlay[base_index + 4] * source_image_height)
            box_right = int(object_info_overlay[base_index + 5] * source_image_width)
            box_bottom = int(object_info_overlay[base_index + 6] * source_image_height)
            label_text = LABELS[int(class_id)] + " (" + str(percentage) + "%)"

            box_color = (255, 128, 0)
            box_thickness = 1
            cv2.rectangle(color_image, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)

            label_background_color = (125, 175, 75)
            label_text_color = (255, 255, 255)

            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            label_left = box_left
            label_top = box_top - label_size[1]
            if (label_top < 1):
                label_top = 1
            label_right = label_left + label_size[0]
            label_bottom = label_top + label_size[1]
            cv2.rectangle(color_image, (label_left - 1, label_top - 1), (label_right + 1, label_bottom + 1), label_background_color, -1)
            cv2.putText(color_image, label_text, (label_left, label_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 1)

        cv2.putText(color_image, fps,       (width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        cv2.putText(color_image, detectfps, (width-170,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)

        cv2.namedWindow('USB Camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('USB Camera', cv2.resize(color_image, (width, height)))

        if cv2.waitKey(1)&0xFF == ord('q'):
            break

        # FPS calculation
        framecount += 1
        if framecount >= 15:
            fps       = "(Playback) {:.1f} FPS".format(time1/15)
            detectfps = "(Detection) {:.1f} FPS".format(detectframecount/time2)
            framecount = 0
            detectframecount = 0
            time1 = 0
            time2 = 0
        t2 = time.perf_counter()
        elapsedTime = t2-t1
        time1 += 1/elapsedTime
        time2 += elapsedTime

except:
    import traceback
    traceback.print_exc()

finally:

    print("\n\nFinished\n\n")

