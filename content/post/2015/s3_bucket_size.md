---
title: Retrieving the size of s3 bucket

date: 2015-07-23

categories:
- amazon
tags:
- amazon
- ec2


---

Here is my notes on how to retrieve the size of a bucket.
<!--more-->


Install the program s3cmd

```
sudo apt-get isntall s3cmd
```

Run the below command to specify your amazon key and secret

```
s3cmd --configure

```

Lets say we have a bucket 'mybucket'.
To actually get the size,use this command

```
s3cmd du -H s3://mybucket

```
