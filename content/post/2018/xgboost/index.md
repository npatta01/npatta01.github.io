---
title: Decision Tree
date: 2018-10-30
categories:
    - machine learning
tags:
    - incomplete
description: decision tree
---


My notes on comparing trees
<!--more-->

Simple Decision Tree
```
clf = DecisionTreeClassifier(random_state=0, class_weight={0:1, 1: 15})

```

**AUC**
```
0.84852499342829957
```


# XGBoost
```
params = {
          'objective': 'binary:logistic', 
          'eval_metric': 'auc', 
          'random_state': 84, 
          'silent': True}


model = xgb.train(params, xgb.DMatrix(x1, y1), num_boost_round=50, evals=watchlist, maximize=True, 
                  early_stopping_rounds = 10, verbose_eval=1)



train-auc:0.959987	valid-auc:0.95946

10 minutes
```



```
gcloud ml-engine local train \
  --package-path example \
  --module-name example.train

```


```
TRAINING_PACKAGE_PATH="example"
now=$(date +"%Y%m%d_%H%M%S")
JOB_NAME="np_test_$now"
MAIN_TRAINER_MODULE="example.train"
JOB_DIR="gs://ableto-datateam-temp/models/$JOB_NAME/output/"
PACKAGE_STAGING_PATH="gs://ableto-datateam-temp/models/$JOB_NAME/staging/"
REGION="us-east1"
RUNTIME_VERSION="1.10"
SCALE_TIER="basic"
PYTHON_VERSION=3.5


gcloud ml-engine jobs submit training $JOB_NAME \
  --package-path $TRAINING_PACKAGE_PATH \
  --module-name $MAIN_TRAINER_MODULE \
  --job-dir $JOB_DIR \
  --region $REGION \
  --runtime-version=$RUNTIME_VERSION \
  --python-version=$PYTHON_VERSION \
  --scale-tier $SCALE_TIER


gcloud ml-engine jobs describe $JOB_NAME
gcloud ml-engine jobs stream-logs $JOB_NAME
```


```
JOB_NAME=np-1
gcloud ml-engine jobs submit training $JOB_NAME \
   --config config.yaml

JOB_NAME=np-1

gcloud alpha ml-engine jobs submit training $JOB_NAME --config=config.yaml


MODEL_NAME=nptest
MODEL_VERSION=v1
gcloud ml-engine models create $MODEL_NAME --regions $REGION


gcloud ml-engine versions create nptest \
    --model model_name
    --origin gs://my/trained/model/path
    --runtime-version 1.11


DEPLOYMENT_SOURCE="gs://ableto-datateam-temp/iris_20181015_030219"
gcloud ml-engine versions create $MODEL_VERSION --model $MODEL_NAME --origin $DEPLOYMENT_SOURCE \
--python-version $PYTHON_VERSION --runtime-version $RUNTIME_VERSION


gcloud ml-engine predict --model $MODEL_NAME --text-instances sample.txt

5.1,3.5,1.4,0.2

``` 