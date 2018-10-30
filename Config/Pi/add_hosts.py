from os import system


hosts = ["tarta", "churro"]
prefixes = {"tarta": "192.168.1.", "churro": "192.168.2."}
host_ips = ""
for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        ip = prefixes[host] + str(i)
        host_ips += (f"{ip}\t{hostname}\n")
        # system(f"ssh pi@{hostname}.local < ./install_iperf.sh")

for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        # system(f"ssh pi@{hostname}.local < ./install_iperf.sh")
        execute = (f"\'sudo sh -c \"echo \\\"{host_ips}\\\" >> /etc/hosts\"\'")
        # execute = (f"rm hosts")
        # system(f"ssh pi@{hostname}.local {execute}")

print(execute)
# print(host_ips)