---
title: Installing R-Studio on Ubuntu 15.04
date: 2015-10-04



categories:
- installation
tags:
- installation
- r
- r-studio


---

Here are my notes in installing R on linux
<!-- more -->
1 ) Add R-Cran mirror
You can find mirror urls [here](https://cran.r-project.org/mirrors.html)

Here is one closet to me

```
sudo add-apt-repository 'deb http://cran.mirrors.hoobly.com/bin/linux/ubuntu vivid/'

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
```

2) Install R
```
sudo apt-get update
sudo apt-get install r-base r-base-dev
```

3) Install R-Studio

```
sudo apt-get install libjpeg62 # dependency needed by R-Studio

wget https://download1.rstudio.org/rstudio-0.99.484-amd64.deb
sudo dpkg -i rstudio-0.99.484-amd64.deb
rm rstudio-0.99.484-amd64.deb

```
