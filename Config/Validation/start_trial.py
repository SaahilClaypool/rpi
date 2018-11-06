#! /usr/bin/python3
import os
import time
import sys
import json
import threading
from typing import Dict

if (not (len(sys.argv) == 2 or len(sys.argv) == 3)):
    print(f"error: enter one or two args, you enetered {len(sys.argv)} args")
    exit()


def c(host, cmd):
    """
    turn into remote version of command
    """
    cmd = cmd.replace("&", "")
    cmd = cmd.replace("-t T", f"-t {trial_time}")
    if (host != 'local'):
        cmd_clean = f"ssh {host} "
        cmd_clean += "\"" + cmd + "\""
        return cmd_clean
    return cmd


def exec_cmd(host, cmd):
    new_thread = "&" in cmd
    cmd = c(host, cmd)
    print("command: ", cmd)
    if (new_thread):
        t = threading.Thread(target=lambda : os.system(cmd))
        t.name = f"{host} $ {cmd}"
        t.start()
        return t
    else:
        os.system(cmd)
        return False


def set_cc(host, cc):
    cmd = \
f"""\
sudo sysctl net.core.default_qdisc=fq;
sudo sysctl net.ipv4.tcp_congestion_control={cc};
sudo sysctl net.ipv4.tcp_congestion_control;
"""
    cmd = c(host, cmd);
    print(cmd)
    os.system(cmd)
    pass

config: Dict = json.loads(open(sys.argv[1], 'r').read())
name = config["name"]
trial_time = config["time"]
if (len(sys.argv) > 2):
    name = sys.argv[2]
print(config)

for host, conf in config["setup"].items():
    print(f"Configuring: {host}\n")
    set_cc(host, conf["cc"])
    for command in conf["commands"]:
        exec_cmd(host, command)

# Sleep to allow threads to start process up etc.
time.sleep(3)

run_handles = []
for host, conf in config["run"].items():
    print(f"Running : {host}\n")
    for command in conf["commands"]:
        join_handle = exec_cmd(host, command)
        run_handles.append(join_handle)
# Block and wait for all tasks started in the run phase
for handle in run_handles:
    handle.join()

for host, conf in config["finish"].items():
    print(f"Running : {host}\n")
    for command in conf["commands"]:
        exec_cmd(host, command)
for host, conf in config["run"].items():
    cc = config["setup"][host]["cc"]
    cmd = f"scp {host}:~/pcap.pcap Results/{name}_{cc}_{host}.pcap"
    print("running: ", cmd)
    os.system(cmd)

os.system("sh ./10mbps_enp3_off.sh")