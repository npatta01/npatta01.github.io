---
title: Optimizing import large sql dump

date: 2015-08-18

categories:
- optimization
tags:
- mysql
- innodb

---

I recently wanted to import a large dump of github data provided by ghtorrent[http://ghtorrent.org/] .
<!-- more -->
The data was 99GB and I wanted to know the progress.

There is a cli tool called [pv](http://linux.die.net/man/1/pv) that gives progress of the dump file read.

So, one can use

```
pv sqlfile.sql | mysql -uxxx -pxxxx dbname
```

Another tip, I learned was that the default mysql options are not optimized for your system config.

This [site](https://tools.percona.com/wizard) provides a wizard to get an optimal mysql config options for your system. The tool is maintained by Percona,service provider built on top of mysql.

My references:
[Source 1](http://dba.stackexchange.com/questions/17367/how-can-i-monitor-the-progress-of-an-import-of-a-large-sql-file)
