sudo tc qdisc del dev enp5s0 root
sudo tc qdisc add dev enp5s0 root handle 1:0 netem delay 100ms
sudo tc qdisc add dev enp5s0 parent 1:1 handle 10: tbf rate 256kbit buffer 1600 limit 5000
tc -s qdisc ls dev enp5s0

# https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
# https://wiki.linuxfoundation.org/networking/netem