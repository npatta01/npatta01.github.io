---
title: Scheduling Jobs
date: 2021-01-07
tags: 
    - scheduling
categories:
    - etl
---

Here is an alternative to using cron.

<!--more-->

```
import schedule
import time
import os

def job():
    print("I'm working...")
    os.system ( "bash /home/nup0013/code/task.sh" )

#schedule.every(2).minutes.do(job)
#schedule.every().hour.do(job)
schedule.every().day.at("11:00").do(job)
schedule.every().day.at("16:00").do(job)


#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


#job()
```