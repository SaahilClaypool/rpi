from os import system
import sys

hosts = ["tarta", "churro"]
command = "echo.sh"
should_run_on_pc = False
if (len(sys.argv) > 1):
    command = sys.argv[1]

if (len(sys.argv) > 2):
    should_run_on_pc = True

for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        system(f"ssh pi@{hostname}.local < {command}")

if (should_run_on_pc):
    for host in hosts:
        hostname = host+"-pc"
        system(f"ssh pc@{hostname} < {command}")

