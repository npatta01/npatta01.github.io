---
title: SSH Mount remote system

date: 2015-09-02

categories:
- hacks
tags:
- ssh
- hacks


---

One way to transfer a file to a remote server is using scp.
```
scp -P 22 path_to_file_locally username@domain:~/
```


If the ssh server, is listening on the default port, you can remove the -P flag.

If you use an ssh config file, you can replace username@domain, with the alias created in the file.
So,
```
scp  path_to_file_locally home:~/
```

It might be nice, if we could have the remote folder mounted locally so, we can edit files with a gui.

One way to do such a thing is using ssfs.
<!-- more -->

In ubuntu, you can connect

```
sudo apt-get install sshfs
sudo modprobe fuse
```

Create a folder for it
```
mkdir ~/remote
```

Mount the file file system
```
sshfs <username>@<ipaddress>:/remotepath ~/remote
```

if using an alias, you can do
```
sshfs home:/remotepath ~/remote
```

If everything, works the folder remote path will be mounted to the remote folder locally.

Any changes you make to the folder remote, will automatically be synced.

If you need to umount the ssh mount, you can use

```
fusermount -u /remotepath
```

If you have a weak connection, and want it to reconnect automatically, you can use
```
sshfs -o follow_symlinks,nonempty,reconnect,ServerAliveInterval=15,ServerAliveCountMax=3 home:/remotepath ~/remote


```
