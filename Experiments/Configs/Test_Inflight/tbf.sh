sudo tc qdisc del dev enp2s0 root

sudo tc qdisc add dev enp2s0 root handle 1:0 netem delay 10ms limit 1000
sudo tc qdisc add dev enp2s0 parent 1:1 handle 10: tbf rate 80mbit buffer 1mbit limit 1000mbit 
sudo tc qdisc add dev enp2s0 parent 10:1 handle 100: tbf rate 80mbit burst .05mbit limit 1000mbit 
# sudo tc qdisc add dev enp2s0 parent 100:1 handle 1000: tbf rate 80mbit burst .05mbit limit 1000mbit 

tc -s qdisc ls dev enp2s0

# https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
# https://wiki.linuxfoundation.org/networking/netem
