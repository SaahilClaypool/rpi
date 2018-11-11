sudo tc qdisc del dev enp3s0 root
sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 10ms
# In the line below, rate is standard rate. burst is amount of tokens available, limit is the queue
sudo tc qdisc add dev enp3s0 parent 1:1 handle 10: tbf rate 80mbit buffer 800mbit limit 10000mbit peakrate 100mbit mtu 1500
# sudo tc qdisc add dev enp3s0 parent 10:1 handle 20: pfifo limit 5000

tc -s qdisc ls dev enp3s0

# https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
# https://wiki.linuxfoundation.org/networking/netem
