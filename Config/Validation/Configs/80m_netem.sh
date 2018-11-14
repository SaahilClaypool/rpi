sudo tc qdisc del dev enp3s0 root
sudo tc qdisc add dev enp3s0 root handle 1:0 netem rate 80mbit delay 10ms limit 10000
tc -s qdisc ls dev enp3s0

# https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
# https://wiki.linuxfoundation.org/networking/netem
