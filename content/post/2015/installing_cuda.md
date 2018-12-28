---
title: Installing cuda 7.5 on Ubuntu 15.04

date: 2015-08-08

categories:
- cuda
tags:
- cuda
- deeplearning

---
Notes on setting up cuda on an ubuntu machine.
<!--more-->



1 ) Download cuda 7.5 [deb](http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda-repo-ubuntu1504-7-5-local_7.5-18_amd64.deb)

2) Install cuda

```
sudo dpkg -i cuda-repo-ubuntu1504-7-5-local_7.5-18_amd64.deb
sudo apt-get update
sudo apt-get install cuda
```

3) Add cuda to path

nano ~/.bashrc
```
export CUDA_HOME=/usr/local/cuda-7.5
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64

PATH=${CUDA_HOME}/bin:${PATH}
export PATH
```

4) (optional) check cuda works
make a copy of the samples and build them

```
rsync -av /usr/local/cuda/samples  .
cd samples/
make -j4
bin/x86_64/linux/release/deviceQuery

```

Hopefully you will see a message containing

Detected 1 CUDA Capable device(s)


5) Download Cuda DNN
Nvidia's DNN can speed up the neural net learning

You need to do a free registration

6) Install Cuda DNN

```
tar -xvf cudnn-7.0-linux-x64-v3.0-prod.tgz
sudo cp lib64/* /usr/local/cuda/lib64/
sudo cp include/* /usr/local/cuda/include/

```

7)  Install cnnem
```
cd cnmem
mkdir build
cd build
cmake ..
make
sudo cp include/cnmem.h /usr/local/cuda/include
sudo cp build/*.so  /usr/local/cuda/lib64/

```

8)
