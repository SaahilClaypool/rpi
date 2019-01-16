sudo tc qdisc del dev enp3s0 root
sleep 5
sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 24ms limit 5000
sudo tc qdisc add dev enp3s0 parent 1:1 handle 10: tbf rate 80mbit buffer 1mbit limit 10000mbit
sudo tc qdisc add dev enp3s0 parent 10:1 handle 100: tbf rate 80mbit burst .05mbit limit 230000b
sudo tc -s qdisc ls dev enp3s0

