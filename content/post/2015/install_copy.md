---
title: Installing copy on Ubuntu 14.04

date: 2015-09-11

categories:
- installation
tags:
- copy
- installation
- backup

---

One service, that I like using to keep my data in sync with multiple computers is [Copy](https://www.copy.com/page/); a servcie that provides 15GB of storage

Here are my notes on how to install it.
<!--more-->

1 ) Run the below on the teminal
```
sudo add-apt-repository ppa:paolorotolo/copy
sudo apt-get update
sudo apt-get install copy
```

2) Create an account

3) Update ulimits
The ulimts (monitoring files) by default in ubuntu are little low for Copy.

Create the file
```
sudo nano /etc/sysctl.d/60-copy.conf
```

Enter the contents in the file
```
fs.inotify.max_user_watches = 20000
fs.file-max = 100000
```

run
```
sudo sysctl -p /etc/sysctl.d/60-copy.conf
```

Note : If the above doesn't work, try running the below commands

```
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```



References
[askubuntu](http://askubuntu.com/questions/454936/copy-app-error-the-open-file-ulimit-level-is-too-low-please-increase-it-other)
[source 2](http://tranduyhung.joomla.com/18-copy-on-linux-the-open-file-ulimit-level-is-too-low-please-increase-it-otherwise-changes-will-not-be-detected-properly)
