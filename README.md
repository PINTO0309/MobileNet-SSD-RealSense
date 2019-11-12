# MobileNet-SSD-RealSense
RaspberryPi3(Raspbian Stretch) or Ubuntu16.04/UbuntuMate + Neural Compute Stick(NCS/NCS2) + RealSense D435(or USB Camera or PiCamera) + MobileNet-SSD(MobileNetSSD)  

**【Notice】December 19, 2018 OpenVINO has supported RaspberryPi + NCS2 !!  
https://software.intel.com/en-us/articles/OpenVINO-RelNotes#inpage-nav-2-2**  
  
**【Dec 31, 2018】 `USB Camera + MultiStick + MultiProcess mode` correspondence with NCS2 is completed.**<br>
**【Jan 04, 2019】 Tune performance four times. MultiStickSSDwithRealSense_OpenVINO_NCS2.py. Core i7 -> NCS2 x1, 48 FPS**<br>
**【Nov 12, 2019】 Compatible with OpenVINO 2019 R3 + RaspberryPi3/4 + Raspbian Buster.**<br>
<br><br>
Measure the distance to the object with RealSense D435 while performing object detection by MobileNet-SSD(MobileNetSSD) with RaspberryPi 3 boosted with Intel Movidius Neural Compute Stick.<br>
"USB Camera mode / PiCamera mode" can not measure the distance, but it operates at high speed.<br>
And, This is support for MultiGraph and FaceDetection, MultiProcessing, Background transparentation.<br>
And, This is support for simple clustering function. (To prevent thermal runaway)<br><br>
## My blog
**【Japanese Article1】  
[RaspberryPi3 (Raspbian Stretch) + Intel Movidius Neural Compute Stick(NCS) + RealSenseD435 + MobileNet-SSD(MobileNetSSD) で高速に物体検出しつつ悟空やモニタまでの距離を測る](https://qiita.com/PINTO/items/1828f97d95fdda45f57d)**<br>
**【Japanese / English Article2】  
[Intel also praised me again ヽ(ﾟ∀ﾟ)ﾉ Yeah MobileNet-SSD(MobileNetSSD) object detection and RealSense distance measurement (640x480) with RaspberryPi3 At least 25FPS playback frame rate + 12FPS prediction rate](https://qiita.com/PINTO/items/40abcf33af3ae7ef579d#-english-article)**<br>
**【Japanese / English Article3】  
[Detection rate approx. 30FPS RaspberryPi3 Model B(plus none) is slightly later than TX2, acquires object detection rate of MobilenetSSD and corresponds to MultiModel VOC+WIDER FACE](https://qiita.com/PINTO/items/190daa4fddfd2a21f959#-detection-rate-approx-30fps-raspberrypi3-model-bplus-none-is-slightly-later-than-tx2-acquires-object-detection-rate-of-mobilenetssd-and-corresponds-to-multimodel-vocwider-face)**<br>
**【Japanese Article4】  
[RaspberryPi3で複数のMovidius Neural Compute Stick をシームレスにクラスタ切り替えして高速推論性能を維持しつつ熱暴走(内部温度70℃前後)を回避する](https://qiita.com/PINTO/items/62859125c5381690623c)**<br>
**【Japanese Article5】  
[Caffeで超軽量な "Semantic Segmentation" のモデルを生成する Sparse-Quantized CNN 512x1024_10MB_軽量モデル_その１](https://qiita.com/PINTO/items/127c84319822a0776420)**<br>
**【Japanese / English Article6】  
[Boost RaspberryPi3 with Neural Compute Stick 2 (1 x NCS2) and feel the explosion performance of MobileNet-SSD　(If it is Core i7, 21 FPS)](https://qiita.com/PINTO/items/fc1fcecce4d5600c20bb#boost-raspberrypi3-with-neural-compute-stick-2-1-x-ncs2-and-feel-the-explosion-performance-of-mobilenet-ssdif-it-is-core-i7-21-fps)**<br>
**【Japanese / English Article7】  
[[24 FPS] Boost RaspberryPi3 with four Neural Compute Stick 2 (NCS2) MobileNet-SSD / YoloV3 [48 FPS for Core i7]](https://qiita.com/PINTO/items/94d5557fca9911cc892d#24-fps-boost-raspberrypi3-with-four-neural-compute-stick-2-ncs2-mobilenet-ssd--yolov3-48-fps-for-core-i7)**<br>
**【Japanese / English Article8】  
[[24 FPS, 48 FPS] RaspberryPi3 + Neural Compute Stick 2, The day when the true power of one NCS2 was drawn out and "Goku" became a true "super saiya-jin"](https://qiita.com/PINTO/items/cb7ba1dae4bfc74a5966#24-fps-48-fps-raspberrypi3--neural-compute-stick-2-the-day-when-the-true-power-of-one-ncs2-was-drawn-out-and-goku-became-a-true-super-saiya-jin)**<br><br>

## Table of contents
**1. [Summary](#summary)**  
　**1.1 [Verification environment NCSDK (1)](#verification-environment-1)**  
　**1.2 [Result of detection rate NCSDK (1)](#result-of-detection-rate-1)**  
　**1.3 [Verification environment NCSDK (2)](#verification-environment-2)**  
　**1.4 [Result of detection rate NCSDK (2)](#result-of-detection-rate-2)**  
**2. [Performance comparison as a mobile application (Based on sensory comparison)](#performance-comparison-as-a-mobile-application-based-on-sensory-comparison)**  
**3. [Change history](#change-history)**  
**4. [Motion image](#motion-image)**  
　**4-1. NCSDK ver**  
　　**4-1-1. [RealSense Mode about 6.5 FPS （Synchronous screen drawing）](#realsense-mode-about-65-fps-detection--synchronous-screen-drawing--singlestickssdwithrealsensepy)**  
　　**4-1-2. [RealSense Mode about 25.0 FPS （Asynchronous screen drawing）](#realsense-mode-about-250-fps-asynchronous-screen-drawing--multistickssdwithrealsensepy)**  
　　**4-1-3. [USB Camera Mode MultiStick x4 Boosted 16.0 FPS+ （Asynchronous screen drawing）](#usb-camera-mode-multistick-x4-boosted-160-fps-asynchronous-screen-drawing--multistickssdwithrealsensepy)**  
　　**4-1-4. [RealSense Mode SingleStick about 5.0 FPS（Transparent background / Asynchronous screen drawing](#realsense-mode-singlestick-about-50-fpstransparent-background-in-real-time--asynchronous-screen-drawing--multistickssdwithrealsensepy)**  
　　**4-1-5. [USB Camera Mode MultiStick x3 Boosted （Asynchronous screen drawing / MultiGraph](#usb-camera-mode-multistick-x3-boosted-asynchronous-screen-drawing--multigraphssdfacedetection--facedetection--multistickssdwithrealsensepy)**  
　　**4-1-6. [Simple clustering function (MultiStick / MultiCluster / Cluster switch cycle / Cluster switch temperature)](#simple-clustering-function-multistick--multicluster--cluster-switch-cycle--cluster-switch-temperature)**  
　**4-2. OpenVINO ver**  
　　**4-2-1. [USB Camera Mode NCS2 x 1 Stick + RaspberryPi3（Synchronous screen drawing）](#usb-camera-mode-ncs2-singlestick--raspberrypi3synchronous-screen-drawing--singlestickssdwithusbcamera_openvino_ncs2py)**  
　　**4-2-2. [USB Camera Mode NCS2 x 1 Stick + Core i7（Synchronous screen drawing）](#usb-camera-mode-ncs2-singlestick--core-i7synchronous-screen-drawing--singlestickssdwithusbcamera_openvino_ncs2py)**  
　　**4-2-3. [USB Camera Mode NCS2 x 1 Stick + Core i7（Asynchronous screen drawing）](#usb-camera-mode-ncs2-x-1-stick--core-i7asynchronous-screen-drawing--multistickssdwithrealsense_openvino_ncs2py)**  
　　**4-2-4. [USB Camera Mode NCS2 x 1 Stick + RaspberryPi3（Asynchronous screen drawing）](#usb-camera-mode-ncs2-x-1-stick--raspberrypi3asynchronous-screen-drawing--multistickssdwithrealsense_openvino_ncs2py)**  
　　**4-2-5. [USB Camera Mode NCS2 x 1 Stick + LattePanda Alpha（Asynchronous screen drawing）48 FPS](#usb-camera-mode-ncs2-x-1-stick--lattepanda-alphaasynchronous-screen-drawing--multistickssdwithrealsense_openvino_ncs2py48-fps)**  
　　**4-2-6. [PiCamera Mode NCS2 x 1 Stick + RaspberryPi3（Asynchronous screen drawing）](#picamera-mode-ncs2-x-1-stick--raspberrypi3asynchronous-screen-drawing--multistickssdwithpicamera_openvino_ncs2py)**  
　　**4-2-7. [USB Camera Mode NCS2 x 1 Stick + RaspberryPi4（Asynchronous screen drawing）40 FPS](#usb-camera-mode-ncs2-x-1-stick--raspberrypi4asynchronous-screen-drawing--multistickssdwithusbcamera_openvino_ncs2py)**  
**5. [Motion diagram of MultiStick](#motion-diagram-of-multistick)**  
**6. [Environment](#environment)**  
**7. [Firmware update with Windows 10 PC](#firmware-update-with-windows-10-pc)**  
**8. [Work with RaspberryPi3 (or PC + Ubuntu16.04 / RaspberryPi + Ubuntu Mate)](#work-with-raspberrypi3-or-pc--ubuntu1604--raspberrypi--ubuntu-mate)**  
　**8-1. [NCSDK ver (Not compatible with NCS2)](#1ncsdk-ver-not-compatible-with-ncs2)**  
　**8-2. [OpenVINO ver (Corresponds to NCS2)](#2openvino-ver-corresponds-to-ncs2)**  
**9. [Execute the program](#execute-the-program)**  
**10. [【Reference】 MobileNetv2 Model (Caffe) Great Thanks!!](#reference-mobilenetv2-model-caffe-great-thanks)**  
**11. [Conversion method from Caffe model to NCS model (NCSDK)](#conversion-method-from-caffe-model-to-ncs-model---ncsdk)**  
**12. [Conversion method from Caffe model to NCS model (OpenVINO)](#conversion-method-from-caffe-model-to-ncs-model---openvino)**  
**13. [Construction of learning environment and simple test for model (Ubuntu16.04 x86_64 PC + GPU NVIDIA Geforce)](#construction-of-learning-environment-and-simple-test-for-model-ubuntu1604-x86_64-pc--gpunvidia-geforce)**  
**14. [Reference articles, thanks](#reference-articles-thanks)**  

## Summary
**Performance measurement result each number of sticks. (It is Detection rate. It is not a Playback rate.)**<br>
**The best performance can be obtained with QVGA + 5 Sticks.**<br>
**However, It is important to use a good quality USB camera.**<br><br>
### Verification environment (1)
|No.|Item|Contents|
|:-:|:-|:-|
|1|Video device|USB Camera (No RealSense D435) **ELP-USB8MP02G-L75 $70**|
|2|Auxiliary equipment|(Required) self-powered USB2.0 HUB|
|3|Input resolution|640x480|
|4|Output resolution|640x480|
|5|Execution parameters|$ python3 MultiStickSSDwithRealSense.py -mod 1 -wd 640 -ht 480|
### Result of detection rate (1)
|No.|Stick count|FPS|Youtube Movie|Note|
|:-:|:-|:-|:-|:-|
|1|1 Stick|6 FPS|**https://youtu.be/lNbhutT8hkA**|base line|
|2|2 Sticks|12 FPS|**https://youtu.be/zuJOhKWoLwc**|6 FPS increase|
|3|3 Sticks|16.5 FPS|**https://youtu.be/8UDFIJ1Z4v8**|4.5 FPS increase|
|4|4 Sticks|16.5 FPS|**https://youtu.be/_2xIZ-IZwZc**|No improvement|

### Verification environment (2)
|No.|Item|Contents|
|:-:|:-|:-|
|1|Video device|USB Camera (No RealSense D435) **PlayStationEye $5**|
|2|Auxiliary equipment|(Required) self-powered USB2.0 HUB|
|3|Input resolution|320x240|
|4|Output resolution|320x240|
|5|Execution parameters|$ python3 MultiStickSSDwithRealSense.py -mod 1 -wd 320 -ht 240|
### Result of detection rate (2)
|No.|Stick count|FPS|Youtube Movie|Note|
|:-:|:-|:-|:-|:-|
|1|4 Sticks|　 25 FPS|**https://youtu.be/v-Cei1TW88c**||
|2|5 Sticks|:star: 30 FPS|**https://youtu.be/CL6PTNgWibI**|best performance|

## Performance comparison as a mobile application (Based on sensory comparison)
◯=HIGH, △=MEDIUM, ×=LOW  

|No.|Model|Speed|Accuracy|Adaptive distance|
|:-:|:-|:-:|:-:|:-|
|1|SSD|×|◯|ALL|
|2|**[MobileNet-SSD](https://github.com/PINTO0309/MobileNet-SSD-RealSense.git)**|△|△|Short distance|
|3|**[YoloV3](https://github.com/PINTO0309/OpenVINO-YoloV3.git)**|×|◯|ALL|
|4|**[tiny-YoloV3](https://github.com/PINTO0309/OpenVINO-YoloV3.git)**|◯|×|Long distance|

## Change history
<details><summary>Change history</summary><div>
[July 14, 2018]　Corresponds to NCSDK v2.05.00.02<br>
[July 17, 2018]　Corresponds to OpenCV 3.4.2<br>
[July 21, 2018]　Support for multiprocessing [MultiStickSSDwithRealSense.py]<br>
[July 23, 2018]　Support for USB Camera Mode [MultiStickSSDwithRealSense.py]<br>
[July 29, 2018]　Added steps to build learning environment<br>
[Aug　3, 2018]　Background Multi-transparent mode implementation [MultiStickSSDwithRealSense.py]<br>
[Aug  11, 2018]　CUDA9.0 + cuDNN7.2 compatible with environment construction procedure<br>
[Aug 14, 2018]　Reference of MobileNetv2 Model added to README and added Facedetection Model<br>
[Aug 15, 2018]　Bug Fixed. `MultiStickSSDwithRealSense.py` depth_scale be undefined. Pull Requests merged. Thank you Drunkar!!<br>
[Aug 19, 2018]　【Experimental】 Update Facedetection model [DeepFace] (graph.facedetectXX)<br>
[Aug 22, 2018]　Separate environment construction procedure of "Raspbian Stretch" and "Ubuntu16.04"<br>
[Aug 22, 2018]　【Experimental】 FaceDetection model replaced [resnet] (graph.facedetection)<br>
[Aug 23, 2018]　Added steps to build NCSDKv2<br>
[Aug 25, 2018]　Added "Detection FPS View" [MultiStickSSDwithRealSense.py]<br>
[Sep 01, 2018]　FaceDetection model replaced [Mobilenet] (graph.fullfacedetection / graph.shortfacedetection)<br>
[Sep 01, 2018]　Added support for MultiGraph and FaceDetection mode [MultiStickSSDwithRealSense.py]<br>
[Sep 04, 2018]　Performance measurement result with 5 sticks is posted<br>
[Sep 08, 2018]　To prevent thermal runaway, simple clustering function of stick was implemented.<br>
[Sep 16, 2018]　【Experimental】 Added Semantic Segmentation model [Tensorflow-UNet] (semanticsegmentation_frozen_person.pb)<br>
[Sep 20, 2018]　【Experimental】 Updated Semantic Segmentation model [Tensorflow-UNet]<br>
[Oct 07, 2018]　【Experimental】 Added Semantic Segmentation model [caffe-jacinto] (cityscapes5_jsegnet21v2_iter_60000.caffemodel)<br>
[Oct 10, 2018]　Corresponds to NCSDK 2.08.01<br>
[Oct 12, 2018]　【Experimental】 Added Semantic Segmentation model [Tensorflow-ENet] (semanticsegmentation_enet.pb) https://github.com/PINTO0309/TensorFlow-ENet.git<br>
[Dec 22, 2018]　Only "USB Camera + single thread mode" correspondence with NCS 2 is completed<br>
[Dec 31, 2018]　"USB Camera + MultiStick + MultiProcess mode" correspondence with NCS2 is completed<br>
[Jan 04, 2019]　Tune performance four times. MultiStickSSDwithRealSense_OpenVINO_NCS2.py<br>
[Feb 01, 2019]　Pull request merged. Fix Typo. Thanks, nguyen-alexa!!<br>
[Feb 09, 2019]　Corresponds to PiCamera.<br>
[Feb 10, 2019]　Added support for SingleStickSSDwithRealSense_OpenVINO_NCS2.py<br>
[Feb 10, 2019]　Firmware v5.9.13 -> v5.10.6, RealSenseSDK v2.13.0 -> v2.16.5<br>
[May 01, 2019]　Corresponds to OpenVINO 2019 R1.0.1<br>
[Nov 12, 2019]　Corresponds to OpenVINO 2019 R3.0<br>
</div></details><br><br>

## Motion image
### **RealSense Mode about 6.5 FPS （Detection + Synchronous screen drawing / SingleStickSSDwithRealSense.py）**<br>
**【YouTube Movie】 https://youtu.be/77cV9fyqJ1w**<br><br>
![03](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/03.gif)
![04](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/04.png)<br><br>
### **RealSense Mode about 25.0 FPS （Asynchronous screen drawing / MultiStickSSDwithRealSense.py）**<br>
**However, the prediction rate is fairly low.(about 6.5 FPS)**<br>
**【YouTube Movie】 https://youtu.be/tAf1u9DKkh4**<br><br>
![09](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/09.gif)<br><br>
### **USB Camera Mode MultiStick x4 Boosted 16.0 FPS+ （Asynchronous screen drawing / MultiStickSSDwithRealSense.py）**<br>
**【YouTube Movie】　https://youtu.be/GedDpAc0JyQ**<br><br>
![10](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/10.gif) ![11](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/11.png)<br>
### **RealSense Mode SingleStick about 5.0 FPS（Transparent background in real time / Asynchronous screen drawing / MultiStickSSDwithRealSense.py）**<br>
**【YouTube Movie】　https://youtu.be/ApyX-mN_dYA**<br><br>
![12](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/12.gif)<br>
### **USB Camera Mode MultiStick x3 Boosted （Asynchronous screen drawing / MultiGraph(SSD+FaceDetection) / FaceDetection / MultiStickSSDwithRealSense.py）**<br>
**【YouTube Movie】　https://youtu.be/fQZpuD8mWok**<br><br>
![13](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/13.gif)<br>
### **Simple clustering function (MultiStick / MultiCluster / Cluster switch cycle / Cluster switch temperature)**<br>
![14](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/14.png)<br>
**[Execution log]**<br>
![15](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/15.png)
### **USB Camera Mode NCS2 SingleStick + RaspberryPi3（Synchronous screen drawing / SingleStickSSDwithUSBCamera_OpenVINO_NCS2.py）**<br>
**【YouTube Movie】　https://youtu.be/GJNkX-ZBuC8**<br><br>
![16](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/16.gif)<br>
### **USB Camera Mode NCS2 SingleStick + Core i7（Synchronous screen drawing / SingleStickSSDwithUSBCamera_OpenVINO_NCS2.py）**<br>
**【YouTube Movie】　https://youtu.be/1ogge90EuqI**<br><br>
![17](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/17.gif)<br>
### **USB Camera Mode NCS2 x 1 Stick + Core i7（Asynchronous screen drawing / MultiStickSSDwithRealSense_OpenVINO_NCS2.py）**<br>
**【YouTube Movie】　https://youtu.be/Nx_rVDgT8uY**<br>
```bash
$ python3 MultiStickSSDwithRealSense_OpenVINO_NCS2.py -mod 1 -numncs 1
```
![23](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/23.gif)<br>
### **USB Camera Mode NCS2 x 1 Stick + RaspberryPi3（Asynchronous screen drawing / MultiStickSSDwithRealSense_OpenVINO_NCS2.py）**<br>
**【YouTube Movie】　https://youtu.be/Xj2rw_5GwlI**<br>
```bash
$ python3 MultiStickSSDwithRealSense_OpenVINO_NCS2.py -mod 1 -numncs 1
```
![24](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/24.gif)<br>
### **USB Camera Mode NCS2 x 1 Stick + LattePanda Alpha（Asynchronous screen drawing / MultiStickSSDwithRealSense_OpenVINO_NCS2.py）[48 FPS]**<br>
**https://twitter.com/PINTO03091/status/1081575747314057219**<br>
### **PiCamera Mode NCS2 x 1 Stick + RaspberryPi3（Asynchronous screen drawing / MultiStickSSDwithPiCamera_OpenVINO_NCS2.py）**<br>
```bash
$ python3 MultiStickSSDwithPiCamera_OpenVINO_NCS2.py
```
![25](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/25.gif)<br>
### **USB Camera Mode NCS2 x 1 Stick + RaspberryPi4（Asynchronous screen drawing / MultiStickSSDwithUSBCamera_OpenVINO_NCS2.py）**<br>
```
$ python3 MultiStickSSDwithUSBCamera_OpenVINO_NCS2.py
```
![26](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/26.gif)<br>
<br>
<br>
## Motion diagram of MultiStick
![20](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/20.png)<br>
## Environment
1．RaspberryPi3 + Raspbian Stretch (USB2.0 Port) or RaspberryPi3 + Ubuntu Mate or PC + Ubuntu16.04<br>
2．Intel RealSense D435 (Firmware Ver 5.10.6) or USB Camera or PiCamera [Official stable version firmware](https://realsense.intel.com/intel-realsense-downloads/#firmware)<br>
3．Intel Neural Compute Stick v1/v2 x１piece or more<br>
4-1．OpenCV 3.4.2 (NCSDK)  
4-2．OpenCV 4.1.1-openvino (OpenVINO)  
5．VFPV3 or TBB (Intel Threading Building Blocks)<br>
6．Numpy<br>
7．Python3.5<br>
8．NCSDK v2.08.01 (It does not work with NCSDK v1.　[v1 version is here](https://github.com/PINTO0309/MobileNet-SSD-RealSense/tree/v1.0))<br>
9. OpenVINO 2019 R2.0.1  
10．RealSenseSDK v2.16.5 (The latest version is unstable) [Official stable version SDK](https://realsense.intel.com/intel-realsense-downloads/#firmware)<br>
11．HDMI Display<br>

## Firmware update with Windows 10 PC
1．ZIP 2 types [(1) Firmware update tool for Windows 10](https://downloadmirror.intel.com/27514/eng/Intel%20RealSense%20D400%20Series%20DFU%20Tool%20for%20Windows.zip)　[(2) The latest firmware bin file](https://downloadmirror.intel.com/28237/eng/Intel%C2%AE%20RealSense%E2%84%A2D400%20Series%20Signed%20Production%20Firmware%20v5_10_6.zip) Download and decompress<br>
2．Copy Signed_Image_UVC_5_10_6_0.bin to the same folder as intel-realsense-dfu.exe<br>
3．Connect RealSense D435 to USB port<br>
4．Wait for completion of installation of device driver<br>
5．Execute intel-realsense-dfu.exe<br>
6．「1」 Type and press Enter and follow the instructions on the screen to update<br>
![01](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/01.png)<br>
7．Firmware version check 「2」<br>
![02](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/02.png)

## Work with RaspberryPi3 (or PC + Ubuntu16.04 / RaspberryPi + Ubuntu Mate)
### 1.NCSDK ver (Not compatible with NCS2)
**Use of Virtualbox is not strongly recommended**<br>
[Note] Japanese Article<br>
https://qiita.com/akitooo/items/6aee8c68cefd46d2a5dc<br>
https://qiita.com/kikuchi_kentaro/items/280ac68ad24759b4c091<br>
<br>
[Post of Official Forum]<br>
https://ncsforum.movidius.com/discussion/950/problems-with-python-multiprocessing-using-sdk-2-0-0-4<br>
https://ncsforum.movidius.com/discussion/comment/3921<br>
https://ncsforum.movidius.com/discussion/comment/4316/#Comment_4316<br><br>

1.Execute the following
```bash
$ sudo apt update;sudo apt upgrade
$ sudo reboot
```
2.Extend the SWAP area (RaspberryPi+Raspbian Stretch / RaspberryPi+Ubuntu Mate Only)
```bash
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=2048

$ sudo /etc/init.d/dphys-swapfile restart;swapon -s
```
3.Install NSCDK<br>
```bash
$ sudo apt install python-pip python3-pip
$ sudo pip3 install --upgrade pip
$ sudo pip2 install --upgrade pip

$ cd ~/ncsdk
$ make uninstall
$ cd ~;rm -r -f ncsdk
#=====================================================================================================
# [Oct 10, 2018] NCSDK 2.08.01 , Tensorflow 1.9.0
$ git clone -b ncsdk2 http://github.com/Movidius/ncsdk
#=====================================================================================================
$ cd ncsdk
$ nano ncsdk.conf

#MAKE_NJOBS=1
↓
MAKE_NJOBS=1

$ sudo apt install cython
$ sudo -H pip3 install cython
$ sudo -H pip3 install numpy
$ sudo -H pip3 install pillow
$ make install

$ cd ~
$ wget https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-all-3.5.1.tar.gz
$ tar -zxvf protobuf-all-3.5.1.tar.gz
$ cd protobuf-3.5.1
$ ./configure
$ sudo make -j1
$ sudo make install
$ cd python
$ export LD_LIBRARY_PATH=../src/.libs
$ python3 setup.py build --cpp_implementation 
$ python3 setup.py test --cpp_implementation
$ sudo python3 setup.py install --cpp_implementation
$ sudo ldconfig
$ protoc --version

# Before executing "make examples", insert Neural Compute Stick into the USB port of the device.
$ cd ~/ncsdk
$ make examples -j1
```
**【Reference】https://github.com/movidius/ncsdk**<br>

4.Update udev rule
```bash
$ sudo apt install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
$ sudo apt install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

$ cd /etc/udev/rules.d/
$ sudo wget https://raw.githubusercontent.com/IntelRealSense/librealsense/master/config/99-realsense-libusb.rules
$ sudo udevadm control --reload-rules && udevadm trigger
```
5.Upgrade to "cmake 3.11.4"
```bash
$ cd ~
$ wget https://cmake.org/files/v3.11/cmake-3.11.4.tar.gz
$ tar -zxvf cmake-3.11.4.tar.gz;rm cmake-3.11.4.tar.gz
$ cd cmake-3.11.4
$ ./configure --prefix=/home/pi/cmake-3.11.4
$ make -j1
$ sudo make install
$ export PATH=/home/pi/cmake-3.11.4/bin:$PATH
$ source ~/.bashrc
$ cmake --version
cmake version 3.11.4
```
6.Register LD_LIBRARY_PATH
```bash
$ nano ~/.bashrc
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

$ source ~/.bashrc
```
7.Install TBB (Intel Threading Building Blocks)
```bash
$ cd ~
$ wget https://github.com/PINTO0309/TBBonARMv7/raw/master/libtbb-dev_2018U2_armhf.deb
$ sudo dpkg -i ~/libtbb-dev_2018U2_armhf.deb
$ sudo ldconfig
```
8.Uninstall old OpenCV (RaspberryPi Only)<br>
**[Very Important] The highest performance can not be obtained unless VFPV3 is enabled.**
```bash
$ cd ~/opencv-3.x.x/build
$ sudo make uninstall
$ cd ~
$ rm -r -f opencv-3.x.x
$ rm -r -f opencv_contrib-3.x.x
```
9.Build install "OpenCV 3.4.2" or Install by deb package.<br>
**[Very Important] The highest performance can not be obtained unless VFPV3 is enabled.**<br><br>
**9.1 Build Install (RaspberryPi Only)**
```bash
$ sudo apt update && sudo apt upgrade
$ sudo apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev \
libjasper-dev libavcodec-dev libavformat-dev libswscale-dev \
libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libgtk-3-dev \
libcanberra-gtk* libatlas-base-dev gfortran python2.7-dev python3-dev

$ cd ~
$ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.2.zip
$ unzip opencv.zip;rm opencv.zip
$ wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.2.zip
$ unzip opencv_contrib.zip;rm opencv_contrib.zip
$ cd ~/opencv-3.4.2/;mkdir build;cd build
$ cmake -D CMAKE_CXX_FLAGS="-DTBB_USE_GCC_BUILTINS=1 -D__TBB_64BIT_ATOMICS=0" \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.2/modules \
        -D BUILD_EXAMPLES=OFF \
        -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_opencv_python2=ON \
        -D BUILD_opencv_python3=ON \
        -D WITH_OPENCL=OFF \
        -D WITH_OPENGL=ON \
        -D WITH_TBB=ON \
        -D BUILD_TBB=OFF \
        -D WITH_CUDA=OFF \
        -D ENABLE_NEON:BOOL=ON \
        -D ENABLE_VFPV3=ON \
        -D WITH_QT=OFF \
        -D BUILD_TESTS=OFF ..
$ make -j1
$ sudo make install
$ sudo ldconfig
```
**9.2 Install by deb package (RaspberryPi Only) [I already activated VFPV3 and built it]**
```bash
$ cd ~
$ sudo apt autoremove libopencv3
$ wget https://github.com/PINTO0309/OpenCVonARMv7/raw/master/libopencv3_3.4.2-20180709.1_armhf.deb
$ sudo apt install -y ./libopencv3_3.4.2-20180709.1_armhf.deb
$ sudo ldconfig
```

10.Install Intel® RealSense™ SDK 2.0
```bash
$ cd ~
$ sudo apt update;sudo apt upgrade
$ sudo apt install -y vulkan-utils libvulkan1 libvulkan-dev

# Ubuntu16.04 Only
$ sudo apt install -y mesa-utils* libglu1* libgles2-mesa-dev libopenal-dev gtk+-3.0

# The latest version is unstable
$ cd ~/librealsense/build
$ sudo make uninstall
$ cd ~
$ sudo rm -rf librealsense

$ git clone -b v2.16.5 https://github.com/IntelRealSense/librealsense.git
$ cd ~/librealsense
$ git checkout -b v2.16.5
$ mkdir build;cd build

$ cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release

# For RaspberryPi3
$ make -j1
or
# For LaptopPC
$ make -j8

$ sudo make install
```
11.Install Python binding
```bash
$ cd ~/librealsense/build

#When using with Python 3.x series
$ cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)

OR

#When using with Python 2.x series
$ cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python)

# For RaspberryPi3
$ make -j1
or
# For LaptopPC
$ make -j8

$ sudo make install
```
12.Update PYTHON_PATH
```bash
$ nano ~/.bashrc
export PYTHONPATH=$PYTHONPATH:/usr/local/lib

$ source ~/.bashrc
```
13.RealSense SDK import test
```bash
$ python3
Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
[GCC 6.3.0 20170124] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyrealsense2
>>> exit()
```
14.Installing the OpenGL package for Python
```bash
$ sudo apt-get install -y python-opengl
$ sudo -H pip3 install pyopengl
$ sudo -H pip3 install pyopengl_accelerate
```
15.Installation of the imutils package. (For PiCamera)
```bash
$ sudo apt-get install -y python3-picamera
$ sudo -H pip3 install imutils --upgrade
```
16.Reduce the SWAP area to the default size (RaspberryPi+Raspbian Stretch / RaspberryPi+Ubuntu Mate Only)
```bash
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=100

$ sudo /etc/init.d/dphys-swapfile restart;swapon -s
```
17.Clone a set of resources
```bash
$ git clone https://github.com/PINTO0309/MobileNet-SSD-RealSense.git
```
18.[Optional] Create a RAM disk folder for movie file placement
```bash
$ cd /etc
$ sudo cp fstab fstab_org
$ sudo nano fstab

# Mount "/home/pi/movie" on RAM disk.
# Add below.
tmpfs /home/pi/movie tmpfs defaults,size=32m,noatime,mode=0777 0 0

$ sudo reboot
```
<br>
<br>

### 2.OpenVINO ver (Corresponds to NCS2)
1.Execute the following
```bash
$ sudo apt update;sudo apt upgrade
$ sudo reboot
```
2.Extend the SWAP area (RaspberryPi+Raspbian Stretch / RaspberryPi+Ubuntu Mate Only)
```bash
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=2048

$ sudo /etc/init.d/dphys-swapfile restart;swapon -s
```
3.Install OpenVINO
```bash
$ curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1rBl_3kU4gsx-x2NG2I5uIhvA3fPqm8uE" > /dev/null
$ CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
$ curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1rBl_3kU4gsx-x2NG2I5uIhvA3fPqm8uE" -o l_openvino_toolkit_ie_p_2018.5.445.tgz
$ tar -zxvf l_openvino_toolkit_ie_p_2018.5.445.tgz
$ rm l_openvino_toolkit_ie_p_2018.5.445.tgz
$ sed -i "s|<INSTALLDIR>|$(pwd)/inference_engine_vpu_arm|" inference_engine_vpu_arm/bin/setupvars.sh
$ nano ~/.bashrc
### Add 1 row below
source /home/pi/inference_engine_vpu_arm/bin/setupvars.sh

$ source ~/.bashrc
### Successful if displayed as below
[setupvars.sh] OpenVINO environment initialized

$ sudo usermod -a -G users "$(whoami)"
$ sudo reboot

$ uname -a
Linux raspberrypi 4.14.79-v7+ #1159 SMP Sun Nov 4 17:50:20 GMT 2018 armv7l GNU/Linux

$ sh inference_engine_vpu_arm/install_dependencies/install_NCS_udev_rules.sh
### It is displayed as follows
Update udev rules so that the toolkit can communicate with your neural compute stick
[install_NCS_udev_rules.sh] udev rules installed
```
4.Update udev rule
```bash
$ sudo apt install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
$ sudo apt install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

$ cd /etc/udev/rules.d/
$ sudo wget https://raw.githubusercontent.com/IntelRealSense/librealsense/master/config/99-realsense-libusb.rules
$ sudo udevadm control --reload-rules && udevadm trigger
```
5.Upgrade to "cmake 3.11.4"
```bash
$ cd ~
$ wget https://cmake.org/files/v3.11/cmake-3.11.4.tar.gz
$ tar -zxvf cmake-3.11.4.tar.gz;rm cmake-3.11.4.tar.gz
$ cd cmake-3.11.4
$ ./configure --prefix=/home/pi/cmake-3.11.4
$ make -j1
$ sudo make install
$ export PATH=/home/pi/cmake-3.11.4/bin:$PATH
$ source ~/.bashrc
$ cmake --version
cmake version 3.11.4
```
6.Register LD_LIBRARY_PATH
```bash
$ nano ~/.bashrc
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

$ source ~/.bashrc
```
7.Install Intel® RealSense™ SDK 2.0
```bash
$ cd ~
$ sudo apt update;sudo apt upgrade
$ sudo apt install -y vulkan-utils libvulkan1 libvulkan-dev

# Ubuntu16.04 Only
$ sudo apt install -y mesa-utils* libglu1* libgles2-mesa-dev libopenal-dev gtk+-3.0

# The latest version is unstable
$ cd ~/librealsense/build
$ sudo make uninstall
$ cd ~
$ sudo rm -rf librealsense

$ git clone -b v2.16.5 https://github.com/IntelRealSense/librealsense.git
$ cd ~/librealsense
$ git checkout -b v2.16.5
$ mkdir build;cd build

$ cmake .. -DBUILD_EXAMPLES=false -DCMAKE_BUILD_TYPE=Release

# For RaspberryPi3
$ make -j1
or
# For LaptopPC
$ make -j8

$ sudo make install
```
8.Install Python binding
```bash
$ cd ~/librealsense/build

#When using with Python 3.x series
$ cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)

OR

#When using with Python 2.x series
$ cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python)

# For RaspberryPi3
$ make -j1
or
# For LaptopPC
$ make -j8

$ sudo make install
```
9.Update PYTHON_PATH
```bash
$ nano ~/.bashrc
export PYTHONPATH=$PYTHONPATH:/usr/local/lib

$ source ~/.bashrc
```
10.RealSense SDK import test
```bash
$ python3
Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
[GCC 6.3.0 20170124] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyrealsense2
>>> exit()
```
11.Installing the OpenGL package for Python
```bash
$ sudo apt-get install -y python-opengl
$ sudo -H pip3 install pyopengl
$ sudo -H pip3 install pyopengl_accelerate
```
12.Installation of the imutils package. (For PiCamera)
```bash
$ sudo apt-get install -y python3-picamera
$ sudo -H pip3 install imutils --upgrade
```
13.Reduce the SWAP area to the default size (RaspberryPi+Raspbian Stretch / RaspberryPi+Ubuntu Mate Only)
```bash
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=100

$ sudo /etc/init.d/dphys-swapfile restart;swapon -s
```
14.Clone a set of resources
```bash
$ git clone https://github.com/PINTO0309/MobileNet-SSD-RealSense.git
```
15.[Optional] Create a RAM disk folder for movie file placement
```bash
$ cd /etc
$ sudo cp fstab fstab_org
$ sudo nano fstab

# Mount "/home/pi/movie" on RAM disk.
# Add below.
tmpfs /home/pi/movie tmpfs defaults,size=32m,noatime,mode=0777 0 0

$ sudo reboot
```
<br>
<br>

## Execute the program
```
$ python3 MultiStickSSDwithRealSense.py <option1> <option2> ...

<options>
 -grp MVNC graphs Path. (Default=./)
 -mod Camera Mode. (0:=RealSense Mode, 1:=USB Camera Mode. Defalut=0)
 -wd　Width of the frames in the video stream. (USB Camera Mode Only. Default=320)
 -ht　Height of the frames in the video stream. (USB Camera Mode Only. Default=240)
 -tp　TransparentMode. (RealSense Mode Only. 0:=No background transparent, 1:=Background transparent. Default=0)
 -sd　SSDDetectionMode. (0:=Disabled, 1:=Enabled. Default=1)
 -fd　FaceDetectionMode. (0:=Disabled, 1:=Enabled. Default=0)
 -snc stick_num_of_cluster. Number of sticks to be clustered. (0:=Clustering invalid, n:=Number of sticks Default=0)
 -csc cluster_switch_cycle. Cycle of switching active cluster. (n:=millisecond Default=10000)
 -cst cluster_switch_temperature. Temperature threshold to switch active cluster. (n.n:=temperature(Celsius) Default=65.0)
```
(Example0) **[MobileNet-SSD + Neural Compute Stick + RealSense D435 Mode + Syncronous](#realsense-mode-about-65-fps-detection--synchronous-screen-drawing--singlestickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 SingleStickSSDwithRealSense.py
```


(Example1) **[MobileNet-SSD + Neural Compute Stick + RealSense D435 Mode + Asynchronous](#realsense-mode-about-250-fps-asynchronous-screen-drawing--multistickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py
```

(Example2) **[MobileNet-SSD + Neural Compute Stick + USB Camera Mode + Asynchronous](#usb-camera-mode-multistick-x4-boosted-160-fps-asynchronous-screen-drawing--multistickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py -mod 1 -wd 640 -ht 480
$ python3 MultiStickSSDwithRealSense.py -mod 1 -wd 320 -ht 240
```

(Example3) **[MobileNet-SSD + Neural Compute Stick + RealSense D435 Mode + Asynchronous + Transparent background in real time](#realsense-mode-singlestick-about-50-fpstransparent-background-in-real-time--asynchronous-screen-drawing--multistickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py -tp 1
```

(Example4) **[MobileNet-SSD + FaceDetection + Neural Compute Stick + USB Camera Mode + Asynchronous ](#usb-camera-mode-multistick-x3-boosted-asynchronous-screen-drawing--multigraphssdfacedetection--facedetection--multistickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py -mod 1 -wd 640 -ht 480 -fd 1
```

(Example5) **To prevent thermal runaway, simple clustering function (2 Stick = 1 Cluster)**<br><br>
When a certain cycle or constant temperature is reached, the active cluster switches seamlessly automatically.<br>
You must turn on the clustering enable flag.<br>
The default switch period is 10 seconds, the default temperature threshold is 65°C.<br>
The number, cycle, and temperature of sticks constituting one cluster can be specified by the start parameter.<br>
Depending on your environment, please tune to the optimum parameters yourself.<br><br>
 **[1] Number of all sticks = 5<br>
 [2] stick_num_of_cluster = 2<br>
 [3] cluster_switch_cycle = 10sec (10,000millisec)<br>
 [4] cluster_switch_temperature = 65.0℃**<br>
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py -mod 1 -snc 2 -csc 10000 -cst 65.0
```
**[Simplified drawing of cluster switching]**<br>
![14](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/14.png)<br>
**[Execution log]**<br>
![15](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/15.png)<br><br>

(Example6)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G2 GL (Fake KMS)"
$ realsense-viewer
```
![05](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/05.gif)

(Example7)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/grabcuts
$ rs-grabcuts
```
![06](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/06.gif)

(Example8)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/imshow
$ rs-imshow
```
![07](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/07.gif)

(Example9) MobileNet-SSD(OpenCV-DNN) + RealSense D435 + Without Neural Compute Stick
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/dnn
$ rs-dnn
```
![08](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/08.gif)
<br>
<br>

## 【Reference】 MobileNetv2 Model (Caffe) Great Thanks!!
**https://github.com/xufeifeiWHU/Mobilenet-v2-on-Movidius-stick.git**

## Conversion method from Caffe model to NCS model - NCSDK
```bash
$ cd ~/MobileNet-SSD-RealSense
$ mvNCCompile ./caffemodel/MobileNetSSD/deploy.prototxt -w ./caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel -s 12
$ mvNCCompile ./caffemodel/Facedetection/fullface_deploy.prototxt -w ./caffemodel/Facedetection/fullfacedetection.caffemodel -s 12
$ mvNCCompile ./caffemodel/Facedetection/shortface_deploy.prototxt -w ./caffemodel/Facedetection/shortfacedetection.caffemodel -s 12
```
## Conversion method from Caffe model to NCS model - OpenVINO
```bash
$ cd ~/MobileNet-SSD-RealSense
$ sudo python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py \
--input_model caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel \
--input_proto caffemodel/MobileNetSSD/MobileNetSSD_deploy.prototxt \
--data_type FP16 \
--batch 1
```
or
```bash
$ cd ~/MobileNet-SSD-RealSense
$ sudo python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py \
--input_model caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel \
--input_proto caffemodel/MobileNetSSD/MobileNetSSD_deploy.prototxt \
--data_type FP32 \
--batch 1
```
## Construction of learning environment and simple test for model (Ubuntu16.04 x86_64 PC + GPU[NVIDIA Geforce])
1.**【Example】** Introduction of NVIDIA-Driver, CUDA and cuDNN to the environment with GPU
```
$ sudo apt-get remove nvidia-*
$ sudo apt-get remove cuda-*

$ apt search "^nvidia-[0-9]{3}$"
$ sudo apt install cuda-9.0
$ sudo reboot
$ nvidia-smi

### Download cuDNN v7.2.1 NVIDIA Home Page
### libcudnn7_7.2.1.38-1+cuda9.0_amd64.deb
### libcudnn7-dev_7.2.1.38-1+cuda9.0_amd64.deb
### cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
### cuda-repo-ubuntu1604-9-0-local-cublas-performance-update_1.0-1_amd64.deb
### cuda-repo-ubuntu1604-9-0-local-cublas-performance-update-2_1.0-1_amd64.deb
### cuda-repo-ubuntu1604-9-0-local-cublas-performance-update-3_1.0-1_amd64.deb
### cuda-repo-ubuntu1604-9-0-176-local-patch-4_1.0-1_amd64.deb

$ sudo dpkg -i libcudnn7*
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
$ sudo apt-key add /var/cuda-repo-9-0-local/7fa2af80.pub
$ sudo apt update
$ sudo dpkg -i cuda-repo-ubuntu1604-9*
$ sudo apt update
$ rm libcudnn7_7.2.1.38-1+cuda9.0_amd64.deb;rm libcudnn7-dev_7.2.1.38-1+cuda9.0_amd64.deb;rm cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb;rm cuda-repo-ubuntu1604-9-0-local-cublas-performance-update_1.0-1_amd64.deb;rm cuda-repo-ubuntu1604-9-0-local-cublas-performance-update-2_1.0-1_amd64.deb;rm cuda-repo-ubuntu1604-9-0-local-cublas-performance-update-3_1.0-1_amd64.deb;rm cuda-repo-ubuntu1604-9-0-176-local-patch-4_1.0-1_amd64.deb

$ echo 'export PATH=/usr/local/cuda-9.0/bin:${PATH}' >> ~/.bashrc
$ echo 'export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64:${LD_LIBRARY_PATH}' >> ~/.bashrc
$ source ~/.bashrc
$ sudo ldconfig
$ nvcc -V
$ cd ~;nano cudnn_version.cpp

#include <cudnn.h>
#include <iostream>

int main(int argc, char** argv) {
    std::cout << "CUDNN_VERSION: " << CUDNN_VERSION << std::endl;
    return 0;
}

$ nvcc cudnn_version.cpp -o cudnn_version
$ ./cudnn_version

$ sudo pip2 uninstall tensorflow-gpu
$ sudo pip2 install tensorflow-gpu==1.10.0
$ sudo pip3 uninstall tensorflow-gpu
$ sudo pip3 install tensorflow-gpu==1.10.0
```
2.**【Example】** Introduction of Caffe to environment with GPU
```
$ cd ~
$ sudo apt install libopenblas-base libopenblas-dev
$ git clone https://github.com/weiliu89/caffe.git
$ cd caffe
$ git checkout ssd
$ cp Makefile.config.example Makefile.config
$ nano Makefile.config
```

```
# cuDNN acceleration switch (uncomment to build with cuDNN).
#USE_CUDNN := 1
↓
# cuDNN acceleration switch (uncomment to build with cuDNN).
USE_CUDNN := 1

# Uncomment if you're using OpenCV 3
# OPENCV_VERSION := 3
↓
# Uncomment if you're using OpenCV 3
OPENCV_VERSION := 3

# CUDA directory contains bin/ and lib/ directories that we need.
CUDA_DIR := /usr/local/cuda
↓
# CUDA directory contains bin/ and lib/ directories that we need.
CUDA_DIR := /usr/local/cuda-9.0

# CUDA architecture setting: going with all of them.
# For CUDA < 6.0, comment the lines after *_35 for compatibility.
CUDA_ARCH := -gencode arch=compute_20,code=sm_20 \
             -gencode arch=compute_20,code=sm_21 \
             -gencode arch=compute_30,code=sm_30 \
             -gencode arch=compute_35,code=sm_35 \
             -gencode arch=compute_50,code=sm_50 \
             -gencode arch=compute_52,code=sm_52 \
             -gencode arch=compute_61,code=sm_61
↓
# CUDA architecture setting: going with all of them.
# For CUDA < 6.0, comment the lines after *_35 for compatibility.
CUDA_ARCH := -gencode arch=compute_30,code=sm_30 \
             -gencode arch=compute_35,code=sm_35 \
             -gencode arch=compute_50,code=sm_50 \
             -gencode arch=compute_52,code=sm_52 \
             -gencode arch=compute_61,code=sm_61

# NOTE: this is required only if you will compile the python interface.
# We need to be able to find Python.h and numpy/arrayobject.h.
PYTHON_INCLUDE := /usr/include/python2.7 \
		/usr/lib/python2.7/dist-packages/numpy/core/include
↓
# NOTE: this is required only if you will compile the python interface.
# We need to be able to find Python.h and numpy/arrayobject.h.
PYTHON_INCLUDE := /usr/include/python2.7 \
		/usr/lib/python2.7/dist-packages/numpy/core/include \
                /usr/local/lib/python2.7/dist-packages/numpy/core/include


# Uncomment to support layers written in Python (will link against Python libs)
# WITH_PYTHON_LAYER := 1
↓
# Uncomment to support layers written in Python (will link against Python libs)
WITH_PYTHON_LAYER := 1

# Whatever else you find you need goes here.
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib
↓
# Whatever else you find you need goes here.
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include \
                /usr/include/hdf5/serial
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib \
                /usr/lib/x86_64-linux-gnu/hdf5/serial

# Uncomment to use `pkg-config` to specify OpenCV library paths.
# (Usually not necessary -- OpenCV libraries are normally installed in one of the above $LIBRARY_DIRS.)
# USE_PKG_CONFIG := 1
↓
# Uncomment to use `pkg-config` to specify OpenCV library paths.
# (Usually not necessary -- OpenCV libraries are normally installed in one of the above $LIBRARY_DIRS.)
USE_PKG_CONFIG := 1
```

```
$ rm -r -f build
$ rm -r -f .build_release
$ make superclean
$ make all -j4
$ make test -j4
$ make distribute -j4
$ export PYTHONPATH=/home/<username>/caffe/python:$PYTHONPATH
$ make py
```

3.Download of VGG model [My Example CAFFE_ROOT PATH = "/home/\<username\>/caffe"]
```
$ export CAFFE_ROOT=/home/<username>/caffe
$ cd $CAFFE_ROOT/models/VGGNet
$ wget http://cs.unc.edu/~wliu/projects/ParseNet/VGG_ILSVRC_16_layers_fc_reduced.caffemodel
```

4.Download VOC 2007 and VOC 2012 datasets

```
# Download the data.
$ cd ~;mkdir data;cd data
$ wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar #<--- 1.86GB
$ wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar #<--- 438MB
$ wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar #<--- 430MB

# Extract the data.
$ tar -xvf VOCtrainval_11-May-2012.tar
$ tar -xvf VOCtrainval_06-Nov-2007.tar
$ tar -xvf VOCtest_06-Nov-2007.tar
$ rm VOCtrainval_11-May-2012.tar;rm VOCtrainval_06-Nov-2007.tar;rm VOCtest_06-Nov-2007.tar
```

5.Generate lmdb file
```
$ export CAFFE_ROOT=/home/<username>/caffe
$ cd $CAFFE_ROOT
# Create the trainval.txt, test.txt, and test_name_size.txt in $CAFFE_ROOT/data/VOC0712/
$ ./data/VOC0712/create_list.sh

# You can modify the parameters in create_data.sh if needed.
# It will create lmdb files for trainval and test with encoded original image:
#   - $HOME/data/VOCdevkit/VOC0712/lmdb/VOC0712_trainval_lmdb
#   - $HOME/data/VOCdevkit/VOC0712/lmdb/VOC0712_test_lmdb
# and make soft links at examples/VOC0712/

$ ./data/VOC0712/create_data.sh
```

6.Execution of learning [My Example environment GPU x1, GeForce GT 650M = RAM:2GB]<br><br>
Adjust according to the number of GPU
```
# It will create model definition files and save snapshot models in:
#   - $CAFFE_ROOT/models/VGGNet/VOC0712/SSD_300x300/
# and job file, log file, and the python script in:
#   - $CAFFE_ROOT/jobs/VGGNet/VOC0712/SSD_300x300/
# and save temporary evaluation results in:
#   - $HOME/data/VOCdevkit/results/VOC2007/SSD_300x300/
# It should reach 77.* mAP at 120k iterations.

$ export CAFFE_ROOT=/home/<username>/caffe
$ export PYTHONPATH=/home/<username>/caffe/python:$PYTHONPATH
$ cd $CAFFE_ROOT
$ cp examples/ssd/ssd_pascal.py examples/ssd/BK_ssd_pascal.py
$ nano examples/ssd/ssd_pascal.py
```

```
# Solver parameters.
# Defining which GPUs to use.
gpus = "0,1,2,3"
↓
# Solver parameters.
# Defining which GPUs to use.
gpus = "0"
```

Adjust according to GPU performance (Memory Size) [My Example GeForce GT 650M x1 = RAM:2GB]
```
# Divide the mini-batch to different GPUs.
batch_size = 32
accum_batch_size = 32
↓
# Divide the mini-batch to different GPUs.
batch_size = 1
accum_batch_size = 1
```

Execution
- The learned data is generated in "$CAFFE_ROOT/models/VGGNet/VOC0712/SSD_300x300"
- VGG_VOC0712_SSD_300x300_iter_n.caffemodel
- VGG_VOC0712_SSD_300x300_iter_n.solverstate
```
$ export CAFFE_ROOT=/home/<username>/caffe
$ export PYTHONPATH=/home/<username>/caffe/python:$PYTHONPATH
$ cd $CAFFE_ROOT
$ python examples/ssd/ssd_pascal.py
```

7.Evaluation of learning data (still image)
```
$ export CAFFE_ROOT=/home/<username>/caffe
$ export PYTHONPATH=/home/<username>/caffe/python:$PYTHONPATH
$ cd $CAFFE_ROOT
# If you would like to test a model you trained, you can do:
$ python examples/ssd/score_ssd_pascal.py
```

8.Evaluation of learning data (USB camera)
```
$ export CAFFE_ROOT=/home/<username>/caffe
$ export PYTHONPATH=/home/<username>/caffe/python:$PYTHONPATH
$ cd $CAFFE_ROOT
# If you would like to attach a webcam to a model you trained, you can do:
$ python examples/ssd/ssd_pascal_webcam.py
```

## Reference articles, thanks
https://github.com/movidius/ncappzoo/tree/master/caffe/SSD_MobileNet<br>
https://github.com/FreeApe/VGG-or-MobileNet-SSD<br>
https://github.com/chuanqi305/MobileNet-SSD<br>
https://github.com/avBuffer/MobilenetSSD_caffe<br>
https://github.com/Coldmooon/SSD-on-Custom-Dataset<br>
https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-Installation-Guide#the-gpu-support-prerequisites<br>
https://stackoverflow.com/questions/33962226/common-causes-of-nans-during-training<br>
https://github.com/CongWeilin/mtcnn-caffe<br>
https://github.com/DuinoDu/mtcnn.git<br>
https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826<br>
https://github.com/Mjrovai/OpenCV-Face-Recognition.git<br>
https://github.com/sgxu/face-detection-based-on-caffe.git<br>
https://github.com/RiweiChen/DeepFace.git<br>
https://github.com/KatsunoriWa/eval_faceDetectors<br>
https://github.com/BeloborodovDS/MobilenetSSDFace<br>
https://www.pyimagesearch.com/2018/09/03/semantic-segmentation-with-opencv-and-deep-learning/<br>
https://github.com/TimoSaemann/ENet/tree/master/Tutorial<br>
https://blog.amedama.jp/entry/2017/04/03/235901<br>
https://github.com/NVIDIA/nvidia-docker<br>
https://hub.docker.com/r/nvidia/cuda/<br>
https://www.dlology.com/blog/how-to-run-keras-model-on-movidius-neural-compute-stick/<br>
https://ncsforum.movidius.com/discussion/1106/ncs-temperature-issue<br>
https://github.com/opencv/opencv/wiki/Intel%27s-Deep-Learning-Inference-Engine-backend<br>
https://github.com/opencv/opencv/wiki/Intel%27s-Deep-Learning-Inference-Engine-backend#raspbian-stretch<br>
https://github.com/skhameneh/OpenVINO-ARM64<br>
