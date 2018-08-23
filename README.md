# MobileNet-SSD-RealSense
RaspberryPi3(Raspbian Stretch) or Ubuntu16.04 + Neural Compute Stick(NCS) + RealSense D435(or USB Camera) + MobileNet-SSD(MobileNetSSD)<br><br>
Measure the distance to the object with RealSense D435 while performing object detection by MobileNet-SSD(MobileNetSSD) with RaspberryPi 3 boosted with Intel Movidius Neural Compute Stick.<br><br>
**【Japanese Article1】 https://qiita.com/PINTO/items/1828f97d95fdda45f57d**<br>
**【Japanese / English Article2】 https://qiita.com/PINTO/items/40abcf33af3ae7ef579d**<br><br>


## Change history
[July 14, 2018]　Corresponds to NCSDK v2.05.00.02<br>
[July 17, 2018]　Corresponds to OpenCV 3.4.2<br>
[July 21, 2018]　Support for multiprocessing <MultiStickSSDwithRealSense.py><br>
[July 23, 2018]　Support for USB Camera Mode <MultiStickSSDwithRealSense.py><br>
[July 29, 2018]　Added steps to build learning environment<br>
[Aug　3, 2018]　Background Multi-transparent mode implementation <MultiStickSSDwithRealSense.py><br>
[Aug  11, 2018]　CUDA9.0 + cuDNN7.2 compatible with environment construction procedure<br>
[Aug 14, 2018]　Reference of MobileNetv2 Model added to README and added Facedetection Model<br>
[Aug 15, 2018]　Bug Fixed. ``MultiStickSSDwithRealSense.py`` depth_scale be undefined. Pull Requests merged. Thank you Drunkar!!<br>
[Aug 19, 2018]　~~**【Experimental】** Update Facedetection model [DeepFace] (graph.facedetectXX)~~<br>
[Aug 22, 2018]　**Separate environment construction procedure of "Raspbian Stretch" and "Ubuntu16.04"**<br>
[Aug 22, 2018]　**【Experimental】** FaceDetection model replaced [resnet] (graph.facedetection)<br>

## Motion image
### **RealSense Mode about 6.5 FPS （Detection + Synchronous screen drawing / SingleStickSSDwithRealSense.py）**<br>
**【YouTube Movie】 https://youtu.be/77cV9fyqJ1w**<br><br>
![03](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/03.gif)
![04](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/04.png)<br><br>
### **RealSense Mode about 25.0 FPS （Asynchronous screen drawing / MultiStickSSDwithRealSense.py）**<br>
**However, the prediction rate is fairly low.(about 8.0 FPS - 12.0 FPS)**<br>
**【YouTube Movie】 https://youtu.be/tAf1u9DKkh4**<br><br>
![09](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/09.gif)<br><br>
### **USB Camera Mode MultiStick x4 Boosted（Asynchronous screen drawing / MultiStickSSDwithRealSense.py）**<br>
**【YouTube Movie】　https://youtu.be/GedDpAc0JyQ**<br><br>
![10](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/10.gif) ![11](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/11.png)<br>
### **RealSense Mode SingleStick（Transparent background in real time / Asynchronous screen drawing / MultiStickSSDwithRealSense.py）**<br>
**【YouTube Movie】　https://youtu.be/ApyX-mN_dYA**<br><br>
![12](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/12.gif)<br>

## Environment
1．RaspberryPi3 + Raspbian Stretch (USB2.0 Port) or Ubuntu16.04<br>
2．Intel RealSense D435 (Firmware Ver 5.9.13) or USB Camera<br>
3．Intel Movidius Neural Compute Stick x１piece or more<br>
4．OpenCV3.4.2<br>
5．VFPV3 or TBB (Intel Threading Building Blocks)<br>
6．Numpy<br>
7．Python3.5 (Only MultiStickSSDwithRealSense.py is multiprocessing enabled)<br>
8．NCSDK v2.05.00.02 (It does not work with NCSDK v1.　[v1 version is here](https://github.com/PINTO0309/MobileNet-SSD-RealSense/tree/v1.0))<br>
9．HDMI Display<br>

## Firmware update with Windows 10 PC
1．ZIP 2 types [(1) Firmware update tool for Windows 10](https://downloadmirror.intel.com/27514/eng/Intel%20RealSense%20D400%20Series%20DFU%20Tool%20for%20Windows.zip)　[(2) The latest firmware bin file](https://downloadmirror.intel.com/27924/eng/Intel%C2%AE%20RealSense%E2%84%A2D400%20Series%20Signed%20Production%20Firmware%20v5_9_13.zip) Download and decompress<br>
2．Copy Signed_Image_UVC_5_9_13_0.bin to the same folder as intel-realsense-dfu.exe<br>
3．Connect RealSense D435 to USB port<br>
4．Wait for completion of installation of device driver<br>
5．Execute intel-realsense-dfu.exe<br>
6．「1」 Type and press Enter and follow the instructions on the screen to update<br>
![01](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/01.png)<br>
7．Firmware version check 「2」<br>
![02](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/02.png)


## Work with RaspberryPi3 (or PC + Ubuntu16.04. Use of Virtualbox is not strongly recommended)
1.Execute the following
```
$ sudo apt update;sudo apt upgrade
$ sudo reboot
```
2.Extend the SWAP area (Raspbian Stretch Only)
```
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=2048

$ sudo /etc/init.d/dphys-swapfile restart swapon -s
```
3.Install NSCDK<br>
```
$ sudo apt install python-pip python3-pip
$ cd ~/ncsdk
$ make uninstall
$ cd ~;rm -r -f ncsdk

$ wget https://ncs-forum-uploads.s3.amazonaws.com/ncsdk/ncsdk-02_05_00_02-full/ncsdk-2.05.00.02.tar.gz
$ tar -zxvf ncsdk-2.05.00.02.tar.gz
$ mv ncsdk-2.05.00.02 ncsdk

or

$ git clone -b ncsdk2 http://github.com/Movidius/ncsdk

$ cd ncsdk
$ nano ncsdk.conf

#MAKE_NJOBS=1
↓
MAKE_NJOBS=1

$ sudo apt install cython
$ sudo -H pip3 install cython
$ sudo -H pip3 install numpy
$ sudo -H pip3 install pillow
$ sudo pip3 uninstall tensorflow
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

$ cd ~/ncsdk
$ make install
$ make examples -j1

$ sudo pip3 uninstall tensorflow
$ sudo pip3 install tensorflow==1.10.0
```
**https://github.com/movidius/ncsdk**<br>

4.Update udev rule
```
# Raspbian Stretch
$ sudo apt install -y git libusb-1.0.0 libusb-1.0-0-dev pkg-config at-spi2-core libgtk-3-dev \
mesa-common-dev libdrm-dev libx11-xcb-dev libxcb-dri3-dev libxcb-present-dev libxcb-sync-dev \
libxshmfence-dev libxcb-dri2-0-dev libxcb-glx0-dev libxxf86vm-dev libgl1-mesa-dev

# Ubuntu16.04
$ sudo apt install -y git libssl-dev libusb-1.0.0 libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev at-spi2-core libdrm*

$ cd /etc/udev/rules.d/
$ sudo wget https://raw.githubusercontent.com/IntelRealSense/librealsense/master/config/99-realsense-libusb.rules
$ sudo udevadm control --reload-rules && udevadm trigger
```
5.Upgrade to "cmake 3.11.4"
```
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
```
$ nano ~/.bashrc
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

$ source ~/.bashrc
```
7.Upgrade protobuf version
```
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
$ export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
$ export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3
$ sudo ldconfig
$ protoc --version
```
8.Install TBB (Intel Threading Building Blocks)
```
$ cd ~
$ wget https://github.com/PINTO0309/TBBonARMv7/raw/master/libtbb-dev_2018U2_armhf.deb
$ sudo dpkg -i ~/libtbb-dev_2018U2_armhf.deb
$ sudo ldconfig
```
9.Uninstall old OpenCV
```
$ cd ~/opencv-3.x.x/build
$ sudo make uninstall
$ cd ~
$ rm -r -f opencv-3.x.x
$ rm -r -f opencv_contrib-3.x.x
```
10.Build install "OpenCV 3.4.2" or Install by deb package.<br>
**10.1 Build Install**
```
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
**10.2 Install by deb package**
```
$ cd ~
$ sudo apt autoremove libopencv3
$ wget https://github.com/PINTO0309/OpenCVonARMv7/raw/master/libopencv3_3.4.2-20180709.1_armhf.deb
$ sudo apt install -y ./libopencv3_3.4.2-20180709.1_armhf.deb
$ sudo ldconfig
```

11.Install Intel® RealSense™ SDK 2.0
```
$ cd ~
$ sudo apt update;sudo apt upgrade

# Ubuntu16.04 Only
$ sudo apt install mesa-utils* libglu1* libgles2-mesa-dev libopenal-dev

$ git clone https://github.com/IntelRealSense/librealsense.git
$ cd ~/librealsense;mkdir build;cd build

$ cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release
$ make -j1
$ sudo make install
```
12.Install OpenCV Wrapper
```
$ cd ~/librealsense/wrappers/opencv;mkdir build;cd build
$ cmake ..
$ nano ../latency-tool/CMakeLists.txt
target_link_libraries(rs-latency-tool ${DEPENDENCIES} pthread)

$ make -j $(($(nproc) + 1))
$ sudo make install
```
13.Install Python binding
```
$ cd ~/librealsense/build

#When using with Python 3.x series
$ cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)

OR

#When using with Python 2.x series
$ cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python)

$ make -j1
$ sudo make install
```
14.Update PYTHON_PATH
```
$ nano ~/.bashrc
export PYTHONPATH=$PYTHONPATH:/usr/local/lib

$ source ~/.bashrc
```
15.RealSense SDK import test
```
$ python3
Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
[GCC 6.3.0 20170124] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyrealsense2
>>> exit()
```
16.Installing the OpenGL package for Python
```
$ sudo apt-get install python-opengl
$ sudo -H pip3 install pyopengl
$ sudo -H pip3 install pyopengl_accelerate
```
17.Reduce the SWAP area to the default size (Raspbian Stretch Only)
```
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=100

$ sudo /etc/init.d/dphys-swapfile restart swapon -s
```
18.Clone a set of resources
```
$ git clone https://github.com/PINTO0309/MobileNet-SSD-RealSense.git
```

## Execute the program
```
$ python3 MultiStickSSDwithRealSense.py <option1> <option2> ...

<options>
 -grp MVNC graphs Path. (Default=./)
 -mod Camera Mode. (0:=RealSense Mode, 1:=USB Camera Mode. Defalut=0)
 -wd　Width of the frames in the video stream. (USB Camera Mode Only. Default=320)
 -ht　Height of the frames in the video stream. (USB Camera Mode Only. Default=240)
 -tp　TransparentMode. (RealSense Mode Only. 0:=No background transparent, 1:=Background transparent. Default=0)
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

(Example2) **[MobileNet-SSD + Neural Compute Stick + USB Camera Mode + Asynchronous](#usb-camera-mode-multistick-x4-boostedasynchronous-screen-drawing--multistickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py -mod 1 -wd 640 -ht 480
```

(Example3) **[MobileNet-SSD + Neural Compute Stick + RealSense D435 Mode + Asynchronous + Transparent background in real time](#realsense-mode-singlesticktransparent-background-in-real-time--asynchronous-screen-drawing--multistickssdwithrealsensepy)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 MultiStickSSDwithRealSense.py -tp 1
```

(Example4)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G2 GL (Fake KMS)"
$ realsense-viewer
```
![05](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/05.gif)

(Example5)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/grabcuts
$ rs-grabcuts
```
![06](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/06.gif)

(Example6)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/imshow
$ rs-imshow
```
![07](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/07.gif)

(Example7) MobileNet-SSD(OpenCV-DNN) + RealSense D435 + Without Neural Compute Stick
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/dnn
$ rs-dnn
```
![08](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/08.gif)

# 【Reference】 MobileNetv2 Model (Caffe) Great Thanks!!
**https://github.com/xufeifeiWHU/Mobilenet-v2-on-Movidius-stick.git**

# Conversion method from Caffe model to NCS model
```
$ cd ~/MobileNet-SSD-RealSense
$ mvNCCompile ./caffemodel/MobileNetSSD/deploy.prototxt -w ./caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel -s 12
$ mvNCCompile ./caffemodel/Facedetection/deploy.prototxt -w ./caffemodel/Facedetection/res10_300x300_ssd_iter_140000.caffemodel -s 12
```

# Construction of learning environment and simple test for model (Ubuntu16.04 x86_64 PC + GPU[NVIDIA Geforce])
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

$ sudo dpkg -i libcudnn7_7.2.1.38-1+cuda9.0_amd64.deb
$ sudo dpkg -i libcudnn7-dev_7.2.1.38-1+cuda9.0_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
$ sudo apt-key add /var/cuda-repo-9-0-local/7fa2af80.pub
$ sudo apt update
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-local-cublas-performance-update_1.0-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-local-cublas-performance-update-2_1.0-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-local-cublas-performance-update-3_1.0-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu1604-9-0-176-local-patch-4_1.0-1_amd64.deb
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

$ sudo pip uninstall tensorflow-gpu
$ sudo pip install tensorflow-gpu==1.10.0
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

# Reference article, thanks
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
