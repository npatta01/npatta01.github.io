---

title: Mounting S3 bucket

date: 2015-07-22

categories:
- amazon
tags:
- amazon
- s3


---

Here is my notes on how to mount an s3 bucket as a file system.
<!--more-->

This [link](https://paycointalk.org/topic/159/how-to-mount-aws-s3-bucket-to-ubuntu-server-14-04) helped me.


install necessary packages

	```
	sudo apt-get update
	sudo apt-get install build-essential gcc make automake autoconf libtool pkg-config intltool libglib2.0-dev libfuse-dev libxml2-dev libevent-dev libssl-dev

	```

install package riofs

	cd /opt

	sudo git clone https://github.com/skoobe/riofs.git
	cd riofs
	sudo ./autogen.sh
	sudo ./configure
	sudo make
	sudo make install

edit riofs config to specify amazon s3 container access key and secret


	sudo nano /usr/local/etc/riofs/riofs.conf.xml
	Press Crtl + w to searc the file for AWS Access Key ID and press Enter
	Remove comment syntax <!-- before this section and --> afters the section
	Replace ### AWS Acess Key ID ### with your AWS Access Key ID
	Replace ### AWS Secret Acess Key ### with your AWS Secret Access Key


Run the below set of commands to create a folder for the s3 bucket and mount it

	sudo mkdir ~/S3
	sudo riofs -o "allow_other" -c /usr/local/etc/riofs/riofs.conf.xml BucketName ~/S3

*note : the s3 folder is mounted with root permission
