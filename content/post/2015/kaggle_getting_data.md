---
title: Kaggle Downloading Data

date: 2015-07-29

categories:
- kaggle
tags:
- kaggle



---

There might be instances where you might need to download a Kaggle dataset to another machine, possibly in an amazons ec2 instance.
<!-- more -->
In order to download the data, you need to be logged in.

One solution is to  export your cookies and tell wget to use your cookies when downloading the data

[This](https://chrome.google.com/webstore/detail/cookietxt-export/lopabhfecdfhgogdbojmaicoicjekelh) is a chrome extension you can use to export your cookies.

And here is the command in wget to download the data
```
wget -x -c --load-cookies cookies.txt -P data -nH --cut-dirs=5 https://www.kaggle.com/c/diabetic-retinopathy-detection/download/trainLabels.csv.zip
```

So, the above command will use your exported cookies to download the file to a folder called data.

The option cut-dirs flatten the directories.



This information was based on a helpful post in the kaggle [forums](https://www.kaggle.com/c/diabetic-retinopathy-detection/forums/t/15313/downloading-data/85858)
