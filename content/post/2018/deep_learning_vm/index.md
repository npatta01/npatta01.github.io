---
title: Deep Learning VM On Google Cloud Platform
date: 2018-11-03
tags: 
    - gcp
    - fastai
    - deep learning
categories:
    - infrastructure
    - deep learning
---

In order to get started with deep learning, you need access to GPU.    
Here are some several options to get access to a free GPU.
<!--more-->

My favorite options are:
- [Google Collab](https://colab.research.google.com)
- [Kaggle Kernels](https://www.kaggle.com)

Those options are very limited in how much you can customize the image.
Eventually, you will need to set up your own image.

Setting up a deep learning VM from scratch involves installing below ideally on a ubuntu machine
- nvidia gpu drivers
- nvidia cuda library
- nvidia cudadnn 
- python /anaconda

To help aid in this process, [Jeremy Horward](https://twitter.com/jeremyphoward) created a bash script that automates this process.

```
wget http://files.fast.ai/setup/paperspace
bash paperspace
```


Google Cloud Recently created a base image that contains all these libraries installed.

To get started     

1) Navigate to [Google Cloud Console](https://console.cloud.google.com/)
https://console.cloud.google.com/

2) Search for "Deep Learning VM"
{{< figure src="static/search.png"  >}}



3) Click "Launch on Compute Engine"

4) Choose a zone to launch the machine
Since I live in the US and east coast, I choose us-east1-c.
Not all GPUs a are avaialble in all regions.
Refer to this [link](https://cloud.google.com/compute/docs/gpus/) for uptodate GPU availability

5) Choose Machine Type
Click on Cutomize to choose your machine specs.
Nvidia Tesla K80 is the chepest GPU.
Choose Atleast 4CPU and 15GB if you are doing anything semi serious

{{< figure src="static/machine_type.png"  >}}

Note: Google Allows you to add upto 8GPUS to one machine

6) Choose Base Framework
There are several base images. Choose Tensorflow, pytorch if you need a specific Deep Learning Framwork.

If you are interested, you could also use the base image to include your custom libraries.

{{< figure src="static/framework.png"  >}}

7) Verify your quota
Click on the quoata link, to verify if you have quoata to launch the gpu.

{{< figure src="static/quota.png" >}}

If you don't have a quoata, choose your metric and location.
Select the gpu and click edit quota.

{{< figure src="static/my_quota.png"  >}}

Note: You will need to add your billing info to get approved.

8) Click Deploy

Congrats, you have launched your deep learning vm.

To connect to the jupyter notebook, run 

```
ZONE=us-east1-c
gcloud compute ssh $INSTANCE_NAME --zone ${ZONE} -- -L 8888:localhost:8080
```




This is the set of commands I run to provision and update this machine
```
export IMAGE_FAMILY="pytorch-latest-gpu" 
export ZONE="us-east1-c"
export INSTANCE_TYPE="n1-highmem-8"
export NUM_GPUS=1
export GCP_PROJECT=np-training

export INSTANCE_NAME="dl2"

gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --image-family=$IMAGE_FAMILY \
        --image-project=deeplearning-platform-release \
        --maintenance-policy=TERMINATE \
        --accelerator="type=nvidia-tesla-k80,count=${NUM_GPUS}" \
        --machine-type=$INSTANCE_TYPE \
        --boot-disk-size=30GB \
        --metadata='install-nvidia-driver=True,jupyter-user=ubuntu' \
        --tags=deep-learning,gpu,jupyter \
        --project ${GCP_PROJECT}


gcloud compute --project ${GCP_PROJECT} ssh --zone=$ZONE ubuntu@$INSTANCE_NAME -- -L 8080:localhost:8080


conda install -c fastai fastai -y
```