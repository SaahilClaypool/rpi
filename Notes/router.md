# Router setup

Goal: On a linux machine, enable ip forwarding. Enable dhcp. For each 


## Links: 

- Reserving static IP  

    https://askubuntu.com/questions/392599/how-to-reserve-ip-address-in-dhcp-server

    in the /etc/dhcp3/dhcpd.conf, assign some host (ex. rpi0) some fixed ip. (but, if dns is on, do I need this?) 
    ```conf
    host Accountant {
    hardware ethernet 00:1F:6A:21:71:3F;
    fixed-address 10.0.0.101;
    }
    ```

- setting up router: 
    https://killtacknine.com/building-an-ubuntu-16-04-router-part-1-network-interfaces/

    This looks like a good tutorial

- dhcp
    https://www.tecmint.com/install-dhcp-server-in-ubuntu-debian/

## Horno

### Interfaces: 

WAN             : enp4s0
NIC1 (tarta 1-4): enp3s0
NIC2 (tarta 5-8): enp5s0


### config

#### netplan

```
sudo vim /etc/netplan/netplan...
sudo netplan try
sudo netplan 
```

#### dhcp

```
sudo vim /etc/dhcp/dhcpd.conf
service dhcp restart
```

#### forwarding

https://serverfault.com/questions/201972/linux-gateway-not-forwarding-packets