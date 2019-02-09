import sys
import numpy as np
import cv2
from os import system
import io, time
from os.path import isfile, join
import re
import pyrealsense2 as rs

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

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

net = cv2.dnn.readNet('lrmodel/MobileNetSSD/MobileNetSSD_deploy.xml', 'lrmodel/MobileNetSSD/MobileNetSSD_deploy.bin')
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

try:

    while True:
        t1 = time.perf_counter()

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        height = color_image.shape[0]
        width = color_image.shape[1]

        blob = cv2.dnn.blobFromImage(color_image, 0.007843, size=(300, 300), mean=(127.5,127.5,127.5), swapRB=False, crop=False)
        net.setInput(blob)
        out = net.forward()
        out = out.flatten()

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

        cv2.putText(color_image, fps,       (width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        cv2.putText(color_image, detectfps, (width-170,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', cv2.resize(color_image, (width, height)))

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

    # Stop streaming
    pipeline.stop()
    print("\n\nFinished\n\n")

