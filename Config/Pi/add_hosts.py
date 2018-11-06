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

host_template = """\
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1       {}
"""

for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        # system(f"ssh pi@{hostname}.local < ./install_iperf.sh")
        content = host_template.format(hostname) + host_ips
        # print(content)
        execute = (f"sudo sh -c \"echo \\\"{content}\\\" > /etc/hosts\"")
        # print(execute)
        # execute += (f"sudo sh -c \"echo \\\"{host_ips}\\\" >> /etc/hosts\";")
        # execute = "'" + execute + "'"
        # # execute = (f"rm hosts")
        sh = f"ssh pi@{hostname} '{execute}'"
        system(sh)
        sh = f"ssh pi@{hostname} 'sudo sh -c \"echo nameserver 8.8.8.8 > /etc/resolv.conf\"'"
        system(sh)

        # sh = f"ssh pi@{hostname} ls"
        # print(sh)

# print(sh)
# print(host_ips)