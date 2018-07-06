# MobileNet-SSD-RealSense
RaspberryPi3 + Neural Compute Stick(NCS) + RealSense D435 + MobileNet-SSD

## Windows 10 PCによるFirmwareのアップデート
１．ZIP ２種類 [(1) Windows10用Firmwareアップデートツール](https://downloadmirror.intel.com/27514/eng/Intel%20RealSense%20D400%20Series%20DFU%20Tool%20for%20Windows.zip)　[(2) 最新ファームウェアbinファイル](https://downloadmirror.intel.com/27924/eng/Intel%C2%AE%20RealSense%E2%84%A2D400%20Series%20Signed%20Production%20Firmware%20v5_9_13.zip) をダウンロードして解凍<br>
２．Signed_Image_UVC_5_9_13_0.bin を intel-realsense-dfu.exe と同じフォルダへコピーする<br>
３．RealSenseD435をUSBポートに接続<br>
４．デバイスドライバのインストール完了を待つ<br>
５．intel-realsense-dfu.exe を実行<br>
６．「1」を入力してEnter入力し、画面の指示に従ってアップデート<br>
７．ファームウェアのバージョン確認「2」<br>
![01](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/01.png)
![02](https://github.com/PINTO0309/MobileNet-SSD-RealSense/blob/master/media/02.png)
