# Setting up the ubuntu router

To create the raspberry pi testbed, we needed to set up two subnets. Each subnet of contains 4 raspberry pis connected to switch. Each switch is then connected to a separate network interface on the ubuntu router. The router is responsible for handling routing between these to subnets. 

```
churro1 --| 
          |                         
churro2 ---  |------|                         
          |->|switch| ---                         
churro3 ---  |------|    |                         
          |              |                         
churr04 --|              |                         
                         |     |----------------|                         
                         |     |                |                         
                         <---->| enp3s0         |                         
                               |                |                         
                               | horno    enp4s0|--> WAN
                               |                |                         
                         <---->| enp5s0         |                         
                         |     |                |                         
                         |     |----------------|                         
tarta1 ---|              |                             
          |              |                           
tarta2 ----  |------|    |                                  
          |->|switch| -- |                                   
tarta3 ----  |------|                                   
          |                         
tarta4 ---|                                         

```
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

First, we need to configure [netplan](https://netplan.io). This is the service ubuntu uses to 