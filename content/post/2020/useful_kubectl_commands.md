---
title: Useful Kubectl Commands
date: 2020-06-21
tags: 
    - kubectl
categories:
    - cheatsheet
---

Here are some common kubectl commands that I find myself using.

<!--more-->


### get namespaces
````bash
kubectl get ns
````

### get deployments
````bash
kubectl -n NAMESPACE get pods
````


### get pods
````bash
kubectl -n NAMESPACE get pods 
````

### logs
The below command will returns logs for multiple container with the label
````bash
kubectl -n NAMESPACE logs -c CONTAINER_NAME -l app=LABEL_VALUE -f
````

### describe pod
````bash
kubectl -n NAMESPACE describe pod POD_NAME
````


### ssh to pod
````bash
kubectl -n NAMESPACE exec -it POD_NAME bash
````



