# Setting up the ubuntu router

To create the raspberry pi testbed, we needed to set up two subnets. Each subnet of contains 4 raspberry pis connected to switch. Each switch is then connected to a separate network interface on the ubuntu router. The router is responsible for handling routing between these to subnets. 

```
churro1 --+ 
          |                         
churro2 --+  +------+                         
          +->|switch|----+                        
churro3 --+  +------+    |                         
          |              |                         
churr04 --+              |                         
                         |     +----------------+                         
                         |     |                |                         
                         +<--->| enp5s0         |                         
                               |                |                         
                               | horno    enp4s0|--> WAN
                               |                |                         
                         +<--->| enp3s0         |                         
                         |     |                |                         
                         |     +----------------+                         
tarta1 ---+              |                             
          |              |                           
tarta2 ---+  +------+    |                                  
          +->|switch|----+                                   
tarta3 ---+  +------+                                   
          |                         
tarta4 ---+                                         

```
## Overview

1. Netplan to configure routes
2. DHCP configuration
3. IP Forwarding & NAT

## Requirements

### Hardware

- Server:
    - 3 nic cards: 
        - 1 for WAN
        - 1 for each subnet
- Switches: 2 netgear routers
- Pis: 8 raspberry pi 
    see `./raspberry.md` for configs

### Software

ubuntu 18.04

## Setup

First, we need to configure [netplan](https://netplan.io). This is the service ubuntu uses to configure basic routing rules. Note: this does *not* control the assignment of ip addresses. That is handled in by dhcp (next section).

netplan uses a yaml file defined in /etc/netplan to configure routing settings for each network interface. These rules are defined in the `ethernet` section of the config file. Below is the file we used to configure the panaderia. Ethernet `enp3s0` refers to the first subnet (containing raspberry pis named tarta 1-4) and `enp5s0` refers to the second subnet containing (containing rasperry pis named churro 1-4). The ethernet interface enp4s0 is the default WAN (wide area network) connecting our router to the outside world. This interface is left untouched. 

For each subnet interface, we need to: 
1. disable dhcp (we will use static ip)
2. match the mac address
3. set the addresses that can be reached 
4. set the routes 
    Note: I think we could set the gateway instead.

> sample 01-network-manager-all.yaml
```yaml
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp3s0: # bay 1 - tarta
      dhcp4: no
      dhcp6: no
      match:
        macaddress: 00:0a:f7:0e:ff:c3
      addresses:
        - 192.168.1.100/24
      nameservers:
        addresses: [8.8.8.8]
      routes:
        - to: 192.168.1.0/24
          via: 192.168.1.100
          metric: 100
    enp5s0: # bay 2 - manzana
      dhcp4: no
      dhcp6: no
      match:
        macaddress: 00:0a:f7:16:80:7f
      addresses:
        - 192.168.2.100/24
      nameservers:
        addresses: [8.8.8.8]
      routes:
        - to: 192.168.2.0/24
          via: 192.168.2.100
          metric: 100
    enp4s0: # WAN
      match:
        macaddress: 5c:f9:dd:6a:e7:77
      dhcp4: true
      dhcp6: true
      # routes:
      #   - to: 0.0.0.0/0
      #     via: 0.0.0.0/0
      #     metric: 50
```
Next, we need to configure dhcp to assign ips to the raspberry pis. First, install dhcpd with `sudo apt install isc-dhcp-server` and change the `INTERFACESv4=""` setting in `/etc/default/isc-dhcp-server` to be the interfaces we want to enable dhcp on.

Then, edit the `/etc/dhcp/dhcpd.conf` files configure dhcp. Configure each subnet with a block like

```
subnet 192.168.1.0 netmask 255.255.255.0 {
    option routers 192.168.1.100;
    option subnet-mask 255.255.255.0;
    range 192.168.1.1 192.168.1.99;
}
```

This will assign the machines in the subnet with the given ip range. Each host can be given a static ip with a similar to the one given below. The hardware ethernet is the mac address (found with `ip a`). The fixed-address is the static ip.

```
host churro1 {
   hardware ethernet b8:27:eb:4d:07:f3;
   fixed-address 192.168.2.1;
}
```

Packet forwarding can be set up by editing the `/etc/sysctl.conf` and changing `net.ipv4.ip_forward=0` to `net.ipv4.ip_forward=1`. 

Finally, NAT needs to be set up. This is easy - just set a rule as follows. 

```
sudo iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
```

Make this persistent with 
```sh
apt-get install iptables-persistent
netfilter-persistent save
netfilter-persistent reload
```

## Firewall

To set up the firewall (ufw), we need to allow packet forwarding between the two subnets. This can be done by editting `/etc/default/ufw` and changing `DEFAULT_FORWARD_POLICY` to `DEFAULT_FORWARD_POLICY="ACCEPT"`. Additionally, make sure everything else is "REJECT". 

Enable the firewall with `sudo ufw enable`. Update the rules with 

```sh
sudo ufw enable
sudo ufw allow from 192.168.2.0/24 
sudo ufw allow from 192.168.1.0/24 
sudo ufw allow from 130.215.0.0/16 
sudo ufw allow from 134.174.0.0/16 
sudo ufw allow from 71.174.237.0/24
sudo ufw allow 22/tcp
sudo ufw status
```
