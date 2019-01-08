#!/usr/bin/python3
from os import system
import sys

hosts = ["tarta", "churro"]
file_name = "echo.sh"
should_run_on_pc = False
if (len(sys.argv) > 1):
    file_name = sys.argv[1]

if (len(sys.argv) > 2):
    should_run_on_pc = True

for host in hosts:
    for i in range(1,5):
        hostname = host+str(i)
        system(f"scp {file_name} pi@{hostname}.local:~")

if (should_run_on_pc):
    for host in hosts:
        hostname = host+"-pc"
        system(f"scp {file_name} pc@{hostname}:~")

