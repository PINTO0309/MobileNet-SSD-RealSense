# MobileNet-SSD-RealSense
RaspberryPi3(Raspbian Stretch) + Neural Compute Stick(NCS) + RealSense D435 + MobileNet-SSD<br><br>
Measure the distance to the object with RealSense D435 while performing object detection by MobileNet-SSD with RaspberryPi 3 boosted with Intel Movidius Neural Compute Stick.<br><br>
**【Japanese Article】 https://qiita.com/PINTO/items/1828f97d95fdda45f57d**<br>
**【YouTube Movie】 https://youtu.be/77cV9fyqJ1w**<br><br>

## Motion image
**about 6.5 FPS （Detection + Screen drawing）**<br>
![03](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/03.gif)
![04](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/04.png)

## Environment
1．RaspberryPi3 + Raspbian Stretch (USB2.0 Port)<br>
2．Intel RealSense D435 (Firmware Ver 5.9.13)<br>
3．Intel Movidius Neural Compute Stick x１piece<br>
4．OpenCV3.4.1<br>
5．TBB (Intel Threading Building Blocks)<br>
6．Numpy<br>
7．Python3.5<br>
8．NCSDK v1.12.00 (It does not work with NCSDK v2.04+)<br>
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


## Work with RaspberryPi3
1.Execute the following
```
$ sudo apt update;sudo apt upgrade
$ sudo reboot
```
2.Extend the SWAP area
```
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=2048

$ sudo /etc/init.d/dphys-swapfile restart swapon -s
```
3.Update udev rule
```
$ sudo apt install -y git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev at-spi2-core libdrm*
$ cd /etc/udev/rules.d/
$ sudo wget https://raw.githubusercontent.com/IntelRealSense/librealsense/master/config/99-realsense-libusb.rules
$ sudo udevadm control --reload-rules && udevadm trigger
```
4.Upgrade to "cmake 3.11.4"
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
5.Register LD_LIBRARY_PATH
```
$ nano ~/.bashrc
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

$ source ~/.bashrc
```
6.Upgrade protobuf version
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
7.Install TBB (Intel Threading Building Blocks)
```
$ cd ~
$ wget https://github.com/PINTO0309/TBBonARMv7/raw/master/libtbb-dev_2018U2_armhf.deb
$ sudo dpkg -i ~/libtbb-dev_2018U2_armhf.deb
$ sudo ldconfig
```
8.Uninstall old OpenCV
```
$ cd ~/opencv-3.x.x/build
$ sudo make uninstall
$ cd ~
$ rm -r -f opencv-3.x.x
$ rm -r -f opencv_contrib-3.x.x
```
9.Build install "OpenCV 3.4.1"
```
$ cd ~
$ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.1.zip
$ unzip opencv.zip;rm opencv.zip
$ wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.1.zip
$ unzip opencv_contrib.zip;rm opencv_contrib.zip
$ cd ~/opencv-3.4.1/;mkdir build;cd build
$ cmake -D CMAKE_CXX_FLAGS="-DTBB_USE_GCC_BUILTINS=1 -D__TBB_64BIT_ATOMICS=0" \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.1/modules \
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
        -D WITH_QT=OFF \
        -D BUILD_TESTS=OFF ..
$ make -j1
$ sudo make install
$ sudo ldconfig
```
10.Install Intel® RealSense™ SDK 2.0
```
$ cd ~
$ sudo apt update;sudo apt upgrade
$ sudo apt install git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev \
libglfw3-dev mesa-utils* libglu1*
$ git clone https://github.com/IntelRealSense/librealsense.git
$ cd ~/librealsense;mkdir build;cd build

$ cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release

OR

$ cmake .. -DBUILD_EXAMPLES=true

$ make -j1
$ sudo make install
```
11.Install OpenCV Wrapper
```
$ cd ~/librealsense/wrappers/opencv;mkdir build;cd build
$ cmake ..
$ nano ../latency-tool/CMakeLists.txt
target_link_libraries(rs-latency-tool ${DEPENDENCIES} pthread)

$ make -j $(($(nproc) + 1))
$ sudo make install
```
12.Install Python binding
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
13.Update PYTHON_PATH
```
$ nano ~/.bashrc
export PYTHONPATH=$PYTHONPATH:/usr/local/lib

$ source ~/.bashrc
```
14.RealSense SDK import test
```
$ python3
Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
[GCC 6.3.0 20170124] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyrealsense2
>>> exit()
```
15.Installing the OpenGL package for Python
```
$ sudo apt-get install python-opengl
$ sudo -H pip3 install pyopengl
$ sudo -H pip3 install pyopengl_accelerate
```
16.Reduce the SWAP area to the default size
```
$ sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=100

$ sudo /etc/init.d/dphys-swapfile restart swapon -s
```
17.Clone a set of resources
```
$ git clone https://github.com/PINTO0309/MobileNet-SSD-RealSense.git
```

## Execute the program

(Example0) **[MobileNet-SSD + Neural Compute Stick + RealSense D435](#motion-image)**
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"
$ cd ~/MobileNet-SSD-RealSense
$ python3 SingleStickSSDwithRealSense.py
```

(Example1)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G2 GL (Fake KMS)"
$ realsense-viewer
```
![05](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/05.gif)

(Example2)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/grabcuts
$ rs-grabcuts
```
![06](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/06.gif)

(Example3)
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/imshow
$ rs-imshow
```
![07](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/07.gif)

(Example4) MobileNet-SSD(OpenCV-DNN) + RealSense D435 + Without Neural Compute Stick
```
$ sudo raspi-config
"7.Advanced Options" - "A7 GL Driver" - "G3 Legacy"

$ cd ~/librealsense/wrappers/opencv/build/dnn
$ rs-dnn
```
![08](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/08.gif)


