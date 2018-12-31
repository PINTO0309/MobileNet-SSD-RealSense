import sys
if sys.version_info.major < 3 or sys.version_info.minor < 4:
    print("Please using python3.4 or greater!")
    sys.exit(1)
import pyrealsense2 as rs
import numpy as np
import cv2, io, time, argparse, re
from os import system
from os.path import isfile, join
from time import sleep
import multiprocessing as mp
from openvino.inference_engine import IENetwork, IEPlugin
import heapq

pipeline = None
lastresults = None
threads = []
processes = []
frameBuffer = None
results = None
fps = ""
detectfps = ""
framecount = 0
detectframecount = 0
time1 = 0
time2 = 0
graph_folder = ""
cam = None
camera_mode = 0
camera_width = 320
camera_height = 240
window_name = ""
background_transparent_mode = 0
ssd_detection_mode = 1
face_detection_mode = 0
elapsedtime = 0.0
background_img = None
depth_sensor = None
depth_scale = 1.0
align_to = None
align = None

LABELS = [['background',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor'],
          ['background', 'face']]

def camThread(LABELS, results, frameBuffer, camera_mode, camera_width, camera_height, background_transparent_mode, background_img):
    global fps
    global detectfps
    global lastresults
    global framecount
    global detectframecount
    global time1
    global time2
    global cam
    global window_name
    global depth_scale
    global align_to
    global align

    # Configure depth and color streams
    #  Or
    # Open USB Camera streams
    if camera_mode == 0:
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        profile = pipeline.start(config)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        align_to = rs.stream.color
        align = rs.align(align_to)
        window_name = "RealSense"
    elif camera_mode == 1:
        cam = cv2.VideoCapture(1)
        if cam.isOpened() != True:
            print("USB Camera Open Error!!!")
            sys.exit(0)
        cam.set(cv2.CAP_PROP_FPS, 60)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
        window_name = "USB Camera"

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    while True:
        t1 = time.perf_counter()

        # 0:= RealSense Mode
        # 1:= USB Camera Mode

        if camera_mode == 0:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            if frameBuffer.full():
                frameBuffer.get()
            color_image = np.asanyarray(color_frame.get_data())

        elif camera_mode == 1:
            # USB Camera Stream Read
            s, color_image = cam.read()
            if not s:
                continue
            if frameBuffer.full():
                frameBuffer.get()
            frames = color_image

        height = color_image.shape[0]
        width = color_image.shape[1]
        frameBuffer.put(color_image.copy())
        res = None

        if not results.empty():
            res = results.get(False)
            detectframecount += 1
            imdraw = overlay_on_image(frames, res, LABELS, camera_mode, background_transparent_mode,
                                      background_img, depth_scale=depth_scale, align=align)
            lastresults = res
        else:
            imdraw = overlay_on_image(frames, lastresults, LABELS, camera_mode, background_transparent_mode,
                                      background_img, depth_scale=depth_scale, align=align)

        cv2.imshow(window_name, cv2.resize(imdraw, (width, height)))

        if cv2.waitKey(1)&0xFF == ord('q'):
            # Stop streaming
            if pipeline != None:
                pipeline.stop()
            sys.exit(0)

        ## Print FPS
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


# l = Search list
# x = Search target value
def searchlist(l, x, notfoundvalue=-1):
    if x in l:
        return l.index(x)
    else:
        return notfoundvalue


def inferencer(graph_folder, results, frameBuffer, ssd_detection_mode, face_detection_mode, device_count):

    plugin = None
    net = None
    inferred_request = [0] * device_count
    heap_request = []
    inferred_cnt = 0

    model_xml = join(graph_folder, "MobileNetSSD_deploy.xml")
    model_bin = join(graph_folder, "MobileNetSSD_deploy.bin")
    plugin = IEPlugin(device="MYRIAD")
    net = IENetwork(model=model_xml, weights=model_bin)
    input_blob = next(iter(net.inputs))
    exec_net = plugin.load(network=net, num_requests=device_count)

    while True:

        try:

            if frameBuffer.empty():
                continue
            color_image = frameBuffer.get()
            prepimg = preprocess_image(color_image)

            reqnum = searchlist(inferred_request, 0)
            if reqnum > -1:
                exec_net.start_async(request_id=reqnum, inputs={input_blob: prepimg})
                inferred_request[reqnum] = 1
                inferred_cnt += 1
                if inferred_cnt == sys.maxsize:
                    inferred_request = [0] * device_count
                    heap_request = []
                    inferred_cnt = 0
                heapq.heappush(heap_request, (inferred_cnt, reqnum))

            cnt, dev = heapq.heappop(heap_request)
            if exec_net.requests[dev].wait(0) == 0:
                exec_net.requests[dev].wait(-1)
                out = exec_net.requests[dev].outputs["detection_out"].flatten()
                results.put([out])
                inferred_request[dev] = 0
            else:
                heapq.heappush(heap_request, (cnt, dev))

        except:
            import traceback
            traceback.print_exc()



def preprocess_image(src):

    try:
        img = cv2.resize(src, (300, 300))
        img = img - 127.5
        img = img * 0.007843
        img = img[np.newaxis, :, :, :]     # Batch size axis add
        img = img.transpose((0, 3, 1, 2))  # NHWC to NCHW
        return img
    except:
        import traceback
        traceback.print_exc()



def overlay_on_image(frames, object_infos, LABELS, camera_mode, background_transparent_mode, background_img, depth_scale=1.0, align=None):

    try:

        # 0:=RealSense Mode, 1:=USB Camera Mode
        if camera_mode == 0:
            # 0:= No background transparent, 1:= Background transparent
            if background_transparent_mode == 0:
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()

            elif background_transparent_mode == 1:
                aligned_frames = align.process(frames)
                depth_frame = aligned_frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame()

            depth_dist  = depth_frame.as_depth_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

        elif camera_mode == 1:
            color_image = frames

        if isinstance(object_infos, type(None)):
            # 0:= No background transparent, 1:= Background transparent
            if background_transparent_mode == 0:
                return color_image
            elif background_transparent_mode == 1:
                return background_img

        # Show images
        height = color_image.shape[0]
        width = color_image.shape[1]
        entire_pixel = height * width
        occupancy_threshold = 0.9

        if background_transparent_mode == 0:
            img_cp = color_image.copy()
        elif background_transparent_mode == 1:
            img_cp = background_img.copy()

        for (object_info, LABEL) in zip(object_infos, LABELS):

            drawing_initial_flag = True

            for box_index in range(100):
                if object_info[box_index + 1] == 0.0:
                    break
                base_index = box_index * 7
                if (not np.isfinite(object_info[base_index]) or
                    not np.isfinite(object_info[base_index + 1]) or
                    not np.isfinite(object_info[base_index + 2]) or
                    not np.isfinite(object_info[base_index + 3]) or
                    not np.isfinite(object_info[base_index + 4]) or
                    not np.isfinite(object_info[base_index + 5]) or
                    not np.isfinite(object_info[base_index + 6])):
                    continue

                x1 = max(0, int(object_info[base_index + 3] * height))
                y1 = max(0, int(object_info[base_index + 4] * width))
                x2 = min(height, int(object_info[base_index + 5] * height))
                y2 = min(width, int(object_info[base_index + 6] * width))

                object_info_overlay = object_info[base_index:base_index + 7]

                # 0:= No background transparent, 1:= Background transparent
                if background_transparent_mode == 0:
                    min_score_percent = 60
                elif background_transparent_mode == 1:
                    min_score_percent = 20

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

                # 0:=RealSense Mode, 1:=USB Camera Mode
                if camera_mode == 0:
                    meters = depth_dist.get_distance(box_left+int((box_right-box_left)/2), box_top+int((box_bottom-box_top)/2))
                    label_text = LABEL[int(class_id)] + " (" + str(percentage) + "%)"+ " {:.2f}".format(meters) + " meters away"
                elif camera_mode == 1:
                    label_text = LABEL[int(class_id)] + " (" + str(percentage) + "%)"

                # 0:= No background transparent, 1:= Background transparent
                if background_transparent_mode == 0:
                    box_color = (255, 128, 0)
                    box_thickness = 1
                    cv2.rectangle(img_cp, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)
                    label_background_color = (125, 175, 75)
                    label_text_color = (255, 255, 255)
                    label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                    label_left = box_left
                    label_top = box_top - label_size[1]
                    if (label_top < 1):
                        label_top = 1
                    label_right = label_left + label_size[0]
                    label_bottom = label_top + label_size[1]
                    cv2.rectangle(img_cp, (label_left - 1, label_top - 1), (label_right + 1, label_bottom + 1), label_background_color, -1)
                    cv2.putText(img_cp, label_text, (label_left, label_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 1)

                elif background_transparent_mode == 1:
                    clipping_distance = (meters+0.05) / depth_scale
                    depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
                    fore = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), 0, color_image)

                    area = abs(box_bottom - box_top) * abs(box_right - box_left)
                    occupancy = area / entire_pixel

                    if occupancy <= occupancy_threshold:
                        if drawing_initial_flag == True:
                            img_cp = fore
                            drawing_initial_flag = False
                        else:
                            img_cp[box_top:box_bottom, box_left:box_right] = cv2.addWeighted(img_cp[box_top:box_bottom, box_left:box_right],
                                                                                             0.85,
                                                                                             fore[box_top:box_bottom, box_left:box_right],
                                                                                             0.85,
                                                                                             0)

        cv2.putText(img_cp, fps,       (width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        cv2.putText(img_cp, detectfps, (width-170,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        return img_cp

    except:
        import traceback
        traceback.print_exc()






if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-grp','--graph',dest='graph_folder',type=str,default='./lrmodel/MobileNetSSD/',help='OpenVINO lrmodels Path. (Default=./lrmodel/MobileNetSSD/)')
    parser.add_argument('-mod','--mode',dest='camera_mode',type=int,default=0,help='Camera Mode. (0:=RealSense Mode, 1:=USB Camera Mode. Defalut=0)')
    parser.add_argument('-wd','--width',dest='camera_width',type=int,default=320,help='Width of the frames in the video stream. (USB Camera Mode Only. Default=320)')
    parser.add_argument('-ht','--height',dest='camera_height',type=int,default=240,help='Height of the frames in the video stream. (USB Camera Mode Only. Default=240)')
    parser.add_argument('-tp','--transparent',dest='background_transparent_mode',type=int,default=0,help='TransparentMode. (RealSense Mode Only. 0:=No background transparent, 1:=Background transparent)')
    parser.add_argument('-sd','--ssddetection',dest='ssd_detection_mode',type=int,default=1,help='[Future functions] SSDDetectionMode. (0:=Disabled, 1:=Enabled Default=1)')
    parser.add_argument('-fd','--facedetection',dest='face_detection_mode',type=int,default=0,help='[Future functions] FaceDetectionMode. (0:=Disabled, 1:=Full, 2:=Short Default=0)')
    parser.add_argument('-numncs','--numberofncs',dest='number_of_ncs',type=int,default=1,help='Number of NCS. (Default=1)')

    args = parser.parse_args()

    graph_folder  = args.graph_folder
    camera_mode   = args.camera_mode
    camera_width  = args.camera_width
    camera_height = args.camera_height
    background_transparent_mode = args.background_transparent_mode
    ssd_detection_mode = args.ssd_detection_mode
    face_detection_mode = args.face_detection_mode
    number_of_ncs = args.number_of_ncs

    # 0:=RealSense Mode, 1:=USB Camera Mode
    if camera_mode != 0 and camera_mode != 1:
        print("Camera Mode Error!! " + str(camera_mode))
        sys.exit(0)

    if camera_mode != 0 and background_transparent_mode == 1:
        background_transparent_mode = 0

    if background_transparent_mode == 1:
        background_img = np.zeros((camera_height, camera_width, 3), dtype=np.uint8)

        if face_detection_mode != 0:
            ssd_detection_mode = 0

    if ssd_detection_mode == 0 and face_detection_mode != 0:
        del(LABELS[0])

    try:

        mp.set_start_method('forkserver')
        frameBuffer = mp.Queue(10)
        results = mp.Queue()

        # Start streaming
        p = mp.Process(target=camThread,
                       args=(LABELS, results, frameBuffer, camera_mode, camera_width, camera_height, background_transparent_mode, background_img),
                       daemon=True)
        p.start()
        processes.append(p)

        # Start detection MultiStick
        # Activation of inferencer
        p = mp.Process(target=inferencer,
                       args=(graph_folder, results, frameBuffer, ssd_detection_mode, face_detection_mode, number_of_ncs),
                       daemon=True)
        p.start()
        processes.append(p)

        while True:
            sleep(1)

    except:
        import traceback
        traceback.print_exc()
    finally:
        for p in range(len(processes)):
            processes[p].terminate()

        print("\n\nFinished\n\n")
