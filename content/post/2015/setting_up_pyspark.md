---

title: Setting up pyspark

date: 2015-07-22

categories:
- spark
tags:
- python
- spark


---

Spark is a general-purpose cluster computing system.

Here are some of my notes in setting up:
<!--more-->

- [download](http://spark.apache.org/downloads.html) spark distribution with a package type of 'pre-built for Hadoop 2/6 or later' even though if you don't have hadoop installed
- Set the environment variable SPARK_HOME such as
```
E:\apps\spark\spark-1.4.1-bin-hadoop2.6
```
- set environment variable PYSPARK_SUBMIT_ARGS to
```
--master local[2]
```

- [download](http://hadoop.apache.org/releases.html) hadoop distribution binary

- set HADOOP_HOME to the unzipped folder

- [download](https://github.com/srccodes/hadoop-common-2.2.0-bin) the content of this repo and add them to the hadoop distribution folder (don't replace existing files)


create ipython config

- ipython profile create pyspark
- edit file ~/.ipython/profile_pyspark/startup/00-pyspark-setup.py





``` python
# Configure the necessary Spark environment
import os
import sys

# Spark home
spark_home = os.environ.get('SPARK_HOME', None)

sys.path.insert(0, spark_home + "/python")

# If Spark V1.4.x is detected, then add ' pyspark-shell' to
# the end of the 'PYSPARK_SUBMIT_ARGS' environment variable
spark_release_file = spark_home + "/RELEASE"
if os.path.exists(spark_release_file) and "Spark 1.4" in open(spark_release_file).read():
    pyspark_submit_args = os.environ.get("PYSPARK_SUBMIT_ARGS", "")
    if not "pyspark-shell" in pyspark_submit_args:
        pyspark_submit_args += " pyspark-shell"
    os.environ["PYSPARK_SUBMIT_ARGS"] = pyspark_submit_args

# Add the spark python sub-directory to the path
sys.path.insert(0, spark_home + "/python")

# Add the py4j to the path.
# You may need to change the version number to match your install
sys.path.insert(0, os.path.join(spark_home, "python/lib/py4j-0.8.2.1-src.zip"))

# Initialize PySpark to predefine the SparkContext variable 'sc'
execfile(os.path.join(spark_home, "python/pyspark/shell.py"))

```

This [link](http://ramhiser.com/2015/02/01/configuring-ipython-notebook-support-for-pyspark/) helped me
