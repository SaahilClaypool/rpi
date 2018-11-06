# BBR 1 validation

## Graphs: 

from : https://queue.acm.org/detail.cfm?id=3022184

Rate: 10 mbps 
delay: 40 ms

## tc

- set the bandwidth etc.:
    ```
    sudo tc qdisc add dev enp3s0 root tbf rate 10mbit burst 10mbit latency  40ms
    ```
- disable: 
    ```sh
    sudo tc qdisc del dev enp3s0 root
    ```
- show:
    ```
    sudo tc qdisc show dev enp3s0
    ```

## printing queue

