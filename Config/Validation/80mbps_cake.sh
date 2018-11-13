sudo tc qdisc del dev enp3s0 root
sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 10ms
sudo tc qdisc add dev enp3s0 parent 1:1 handle 10: cake bandwidth 80mbit rtt 10000ms besteffort flowblind
# setting rtt should disable the ecn 

tc -s qdisc ls dev enp3s0
