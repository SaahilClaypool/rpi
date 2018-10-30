from os import system

hosts = ["tarta", "churro"]
for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        system(f"ssh pi@{hostname}.local < ./install_iperf.sh")