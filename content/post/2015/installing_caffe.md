---
title: Installing cuda 7.0 on Ubuntu 14.04

date: 2015-08-04

categories:
- cuda
tags:
- cuda
- deeplearning

---

Using python 2.7/ opencv3
<!--more-->


Was getting error 'undefined cv::imread'[1](https://github.com/BVLC/caffe/issues/2288)
so, I fixed it by editing the Makefile of caffe to add  opencv_imgcodecs

```
LIBRARIES += glog gflags protobuf leveldb snappy \
        lmdb \
        boost_system \
        hdf5_hl hdf5 \
        opencv_imgcodecs opencv_highgui opencv_imgproc opencv_core pthread
```

https://github.com/BVLC/caffe/issues/2288

[2](http://stackoverflow.com/questions/27890137/undefined-symbols-for-architecture-x86-64-for-caffe-build)


added line in Makefile.config and commented the previous line
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial/


https://github.com/BVLC/caffe/issues/2690
Followed the guide from [here](https://github.com/NVIDIA/DIGITS)

https://github.com/BVLC/caffe/issues/1276

export PYTHONPATH=${CAFFE_HOME}/python:$PYTHONPATH


import caffe



CUDNN_STATUS_ARCH_MISMATCH

I solved it commenting both cuDNN and CPU possibilities at the beginning of the Makefile.config file in order to work only with CUDA and then rebuilding the library with the "make clean/all/test/runtest" commands. It shows a message skipping two test samples when running "make test", since they are the cuDNN based samples that I am not using anymore. Then, I was able run the mnist/train_lenet.sh example.


#tell to use theano
echo -e "\n[global]\nfloatX=float32\ndevice=gpu\n[mode]=FAST_RUN\n\n[nvcc]\nfastmath=True\n\n[cuda]\nroot=/usr/local/cuda" >> ~/.theanorc  

pip install theano

http://markus.com/install-theano-on-aws/

python `python -c "import os, theano; print os.path.dirname(theano.__file__)"`/misc/check_blas.py
