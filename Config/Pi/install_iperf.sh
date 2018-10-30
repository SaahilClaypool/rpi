sudo sh -c "echo nameserver 8.8.8.8 > /etc/resolv.conf"
read
sudo apt-get remove iperf3 libiperf0 -y
wget https://iperf.fr/download/ubuntu/iperf3_3.1.3-1_armhf.deb
wget https://iperf.fr/download/ubuntu/libiperf0_3.1.3-1_armhf.deb
sudo dpkg -i libiperf0_3.1.3-1_armhf.deb iperf3_3.1.3-1_armhf.deb 
rm libiperf0_3.1.3-1_armhf.deb iperf3_3.1.3-1_armhf.deb