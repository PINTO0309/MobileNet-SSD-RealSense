# MobileNet-SSD-RealSense
RaspberryPi3 + Neural Compute Stick(NCS) + RealSense D435 + MobileNet-SSD

## Firmware update with Windows 10 PC
１．ZIP 2 types [(1) Firmware update tool for Windows 10](https://downloadmirror.intel.com/27514/eng/Intel%20RealSense%20D400%20Series%20DFU%20Tool%20for%20Windows.zip)　[(2) The latest firmware bin file](https://downloadmirror.intel.com/27924/eng/Intel%C2%AE%20RealSense%E2%84%A2D400%20Series%20Signed%20Production%20Firmware%20v5_9_13.zip) Download and decompress<br>
２．Copy Signed_Image_UVC_5_9_13_0.bin to the same folder as intel-realsense-dfu.exe<br>
３．Connect RealSense D435 to USB port<br>
４．Wait for completion of installation of device driver<br>
５．intel-realsense-dfu.exe を実行<br>
６．「1」 Type and press Enter and follow the instructions on the screen to update<br>
７．Firmware version check 「2」<br>
![01](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/01.png)
![02](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/02.png)
