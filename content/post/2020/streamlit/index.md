---
title: Intro to Streamlit
date: 2020-12-21
tags: 
    - streamlit
categories:
    - cheatsheet
---

Streamlit is a useful framework for building interaction python apps.

<!--more-->

Streamlit apps are python scripts that run from top to bottom. 

Here is the code to display something in the app.

```python
import streamlit as st
st.write('Hello, world!')
```



![Streamlit Hello](static/streamlit_hello.png)

## Displaying options

**Displaying Data**

json
![Streamlit Json](static/display_json.png)

dataframe
![Streamlit dataframe](static/display_df.png)

**Displaying Media**

Chart
![Streamlit Chart](static/display_chart.png)


Image
![Streamlit Image](static/display_image.png)

Video
![Streamlit Video](static/display_video.png)

**Interactive Widgets**

It supports:

- button / checkbox 
- select/ multiselect / slider
- text/numberic input / date
- file uploader

Everything is as simple as 

```python
color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)
```



Apps can be run using 
```bash
streamlit run test.py
```


Here is a simple streamlit app that I build that displays a multi page app.

The Apps displaying an interactive machine learning and visualization dashboard.

![Machine Learning DEmo](https://raw.githubusercontent.com/npatta01/streamlit-demo/main/images/ml_demo.png)

Complete App in Action
![Demo in Action](https://github.com/npatta01/streamlit-demo/raw/main/images/in_action.gif)