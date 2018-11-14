# max speed
sudo ethtool -r enp3s0
sudo tc qdisc del dev enp3s0 root

# sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 10ms limit 10000
# turn down speed
# sudo ethtool -s enp3s0 speed 80 duplex full autoneg off
sudo ethtool -s enp3s0 speed 100 autoneg off
tc -s qdisc ls dev enp3s0

# https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
# https://wiki.linuxfoundation.org/networking/netem
