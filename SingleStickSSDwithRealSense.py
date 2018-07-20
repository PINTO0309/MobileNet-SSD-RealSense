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
from mvnc import mvncapi as mvnc
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

mvnc.global_set_option(mvnc.GlobalOption.RW_LOG_LEVEL, 2)
devices = mvnc.enumerate_devices()
if len(devices) == 0:
    print("No devices found")
    quit()
print(len(devices))

devHandle   = []
graphHandle = []

with open(join(graph_folder, "graph"), mode="rb") as f:
    graph_buffer = f.read()
graph = mvnc.Graph('MobileNet-SSD')

for devnum in range(len(devices)):
    devHandle.append(mvnc.Device(devices[devnum]))
    devHandle[devnum].open()
    graphHandle.append(graph.allocate_with_fifos(devHandle[devnum], graph_buffer))

print("\nLoaded Graphs!!!")


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    #freq = cv2.getTickFrequency()

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

        #dnn
        im = cv2.resize(color_image, (300, 300))
        im = im - 127.5
        im = im * 0.007843

        #graphHandle[0][0]=input_fifo, graphHandle[0][1]=output_fifo
        graph.queue_inference_with_fifo_elem(graphHandle[0][0], graphHandle[0][1], im.astype(np.float32), color_image)
        out, input_image = graphHandle[0][1].read_elem()

        # Show images
        height = color_image.shape[0]
        width = color_image.shape[1]
        num_valid_boxes = int(out[0])

        if num_valid_boxes > 0:

            for box_index in range(num_valid_boxes):
                base_index = 7+ box_index * 7
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
    pipeline.stop()
    for devnum in range(len(devices)):
        graphHandle[devnum][0].destroy()
        graphHandle[devnum][1].destroy()
        graph.destroy()
        devHandle[devnum].close()
        devHandle[devnum].destroy()

    print("\n\nFinished\n\n")
    sys.exit()

