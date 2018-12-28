---
title: Installing python dlib

date: 2015-08-10

categories:
- computer vision
tags:
- dlib
- computer vision

---

[Dlib](http://dlib.net/) is C++ machine learning library

Here are some instructions to install it

<!--more-->

- clone the repo
```
git clone git@github.com:davisking/dlib.git
```
- navigate to the dlib folder
```
cd dlib
```

- (optional)if using a virtual environment, activate it
```
// cv is my virtualenv name

- workon cv
```
- build the python bindings
I neeed to pass the flag 'DLIB_JPEG_SUPPORT' to build jpeg support
```
python setup.py install --yes DLIB_JPEG_SUPPORT
```


Test if everything is working
The python_examples folder has some nice examples of usage.

Lets run the trained facial detector, example
```
python python_examples/face_detector.py examples/faces/2007_007763.jpg
```

If all works, you should see an image with red rectangles around faces.
