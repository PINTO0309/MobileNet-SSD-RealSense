import sys
graph_folder="./"
if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    exit(1)

if len(sys.argv) > 1:
    graph_folder = sys.argv[1]

import pyrealsense2 as rs
import numpy as np
import cv2
#from mvnc import mvncapi as mvnc
from os import system
import io, time
from os.path import isfile, join
import re

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

net = cv2.dnn.readNet('lrmodel/MobileNetSSD/MobileNetSSD_deploy.xml', 'lrmodel/MobileNetSSD/MobileNetSSD_deploy.bin')
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

try:
    #freq = cv2.getTickFrequency()

    while True:
        t1 = time.perf_counter()

        # Read an image
        ret, color_image = cap.read()
        if not ret:
            break

        #dnn
        im = cv2.resize(color_image, (300, 300))
        #im = im - 127.5
        #im = im * 0.007843

        # Prepare input blob and perform an inference
        #blob = cv2.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv2.CV_8U)
        #print(im.depth())
        blob = cv2.dnn.blobFromImage(im, ddepth=cv2.CV_8U)
        net.setInput(blob)

        # Show images
        height = color_image.shape[0]
        width = color_image.shape[1]
        out = net.forward()
        #num_valid_boxes = int(out[0])

        out = out[0]
        print(int(out[0]))
        print(out.shape)
        #print(out)
        sys.exit(0)

        if num_valid_boxes > 0:

            for box_index in range(num_valid_boxes):
                base_index = 7 + box_index * 7
                if (not np.isfinite(out[base_index]) or
                    not np.isfinite(out[base_index + 1]) or
                    not np.isfinite(out[base_index + 2]) or
                    not np.isfinite(out[base_index + 3]) or
                    not np.isfinite(out[base_index + 4]) or
                    not np.isfinite(out[base_index + 5]) or
                    not np.isfinite(out[base_index + 6])):
                    continue

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
                meters = depth_frame.as_depth_frame().get_distance(box_left+int((box_right-box_left)/2), box_top+int((box_bottom-box_top)/2))
                label_text = LABELS[int(class_id)] + " (" + str(percentage) + "%)"+ " {:.2f}".format(meters) + " meters away"

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

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', cv2.resize(color_image,(width, height)))

        ## Print FPS
        t2 = time.perf_counter()
        time1 = (t2-t1)#/freq
        print(" {:.2f} FPS".format(1/time1))

        if cv2.waitKey(1)&0xFF == ord('q'):
            break

except:
    import traceback
    traceback.print_exc()

finally:

    # Stop streaming
    #pipeline.stop()
    #for devnum in range(len(devices)):
    #    graphHandle[devnum][0].destroy()
    #    graphHandle[devnum][1].destroy()
    #    graph.destroy()
    #    devHandle[devnum].close()
    #    devHandle[devnum].destroy()

    print("\n\nFinished\n\n")
    sys.exit()

