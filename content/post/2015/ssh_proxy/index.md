---

title: SSH Tunneling

date: 2015-07-22

categories:
- hacks
tags:
- ssh
- proxy
- ec2


---

Sometimes, you want to access a service running on a remote server, but there might be a firewall that does not forward the traffic to the port.

One way to deal with this is to create a socks proxy.
<!--more-->

If we direct traffic from our computer, to use the proxy, we will be able to access the remote services .

1) Create an ssh tunel/socks proxy

```
ssh -fCND 127.0.0.1:8157 ubuntu@amazonec2host
```

2) Tell your browser to use the proxy
I use Google chrome and like the extension [Proxy Switch Omega](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=en)

The extension, makes it easy to enable and disable chrome from using the proxy.



We can then direct So, all traffic will go to the proxy we created

1) Create a Proxy profile, with the below options

{% asset_img  new_proxy.png [EC2 proxy profile] %}

2) Create a Switch Profile, with the below options
{% asset_img  switch_profile.png [Switch profile] %}

The above settings, tells chrome that every url that matches those patterns to use our proxy.

```
*ec2*.amazonaws.com*
*ec2*.amazonaws.com*
*localhost*
```

Note: The last patterns makes services running locally on your machine inaccesible on localhost:port from the browser while the profile is active. Those services are still accessible on 127.0.0.1:port


3) Tell chrome to use the profile
{% asset_img  choosing_profile.png [Choosing profile] %}

Now, in your browser you can access services running on your remote host on urls like

localhost:8080
amazon_public_ip:8080


If the above too much, and you just want to forward a single port, one can use

```
ssh -L 9000:localhost:5432 user@example.com
```
The above will forward local traffic from port 9000 to the remote server port 5432.
