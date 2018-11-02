from os import system
import sys

hosts = ["tarta", "churro"]
command = "echo.sh"
if (len(sys.argv) > 1):
    command = sys.argv[1]

for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        system(f"ssh pi@{hostname}.local < {command}")