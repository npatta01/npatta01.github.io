---
title: SSH Config file

date: 2015-09-01

categories:
- hacks
tags:
- ssh
- hacks


---
SSH Config file is a way to manage your manage your ssh connections.
<!--more-->



If you have multiple ssh keys, one can connect to a different host using

```
ssh -i ~/.ssh/custom_key  username@host.com
```

Another way to deal with multiple hosts ans keys is to use an ssh config file (~/.ssh/config)

For example, here is how my file looks

```
Host github.com
    User git
    IdentityFile ~/.ssh/id_git
    Port 22

Host home
   Hostname homeserver.duckdns.org
   User ubuntu
   Port 2224
   IdentityFile ~/.ssh/id_homeserver

```

You can ignore the port line above, is the ssh server is listening on port 22.

Now, you can connect to the destination, by using
```
ssh home
```
