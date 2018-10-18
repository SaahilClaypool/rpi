# Raspberry Pi Setup

## Images

pi@rpi0 raspberry 0 

ssh: only works from windows (for local ssh. Should work fine once on network)

sharing internet: https://raspberrypi.stackexchange.com/questions/11684/how-can-i-connect-my-pi-directly-to-my-pc-and-share-the-internet-connection 

## Testing

### Wifi: 

client (rpi): iperf3 -s 
server (win): iperf3.exe -c rpi0.local

results: ~


### IO

## BBR

https://www.techrepublic.com/article/how-to-enable-tcp-bbr-to-improve-network-speed-on-linux/

- Add to `/etc/systctl.conf`

    ```
    net.core.default_qdisc=fq
    net.ipv4.tcp_congestion_control=bbr
    ```
- run `sudo sysctl -p` to reload

- run `sysctl net.ipv4.tcp_congestion_control` to check

    output should be: `net.ipv4.tcp_congestion_control = bbr`
