---
title: Installing opencv 3.0.0 on Ubuntu 14.04

date: 2015-08-04

categories:
- computer vision

tags:
- python
- opencv



---

I recently wanted to get opencv installed on my ubuntu machine.

<!--more-->


I needed to install these optional dependencies.
```
sudo apt-get -y install libopencv-dev build-essential cmake git libgtk2.0-dev pkg-config python-dev python-numpy libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff4-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev libtbb-dev libqt4-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils unzip doxygen ant graphviz  python3-dev tesseract-ocr tesseract-ocr-eng

sudo apt-get install ubuntu-restricted-extras
```

I wanted java bindings, so I set my JAVA_HOME in my .bashrc to the value returned from
```
sudo update-alternatives --config java
```

```
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export JAVA_INCLUDE_PATH=/usr/lib/jvm/java-8-oracle/include
export JAVA_INCLUDE_PATH2=/usr/lib/jvm/java-8-oracle/include/linux
```

Some issues , I have encountered were,
- python 3 modules not build (update cmake)
- opencv not finding python3 lib:
 pass a flag to ubuntu

 PYTHON3_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.4m.so\


I had to update cmake from v2 to v3

```

sudo add-apt-repository ppa:george-edison55/cmake-3.x
sudo apt-get update

sudo apt-get install cmake

sudo apt-get upgrade


```


I then build opencv from source following this [guide](http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/).



My references:
[Source 1](http://rodrigoberriel.com/2014/10/installing-opencv-3-0-0-on-ubuntu-14-04/)

[Source 2](http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/)
