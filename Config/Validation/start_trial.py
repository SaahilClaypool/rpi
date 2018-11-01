import os 
import sys
import json
from typing import Dict

if (len(sys.argv) != 2):
    print("error: enter only one arg")
    exit()

def c(host, cmd):
    """
    turn into remote version of command
    """
    if (host != 'local'):
        cmd_clean = f"ssh {host} "
        cmd_clean += "\"" + cmd + "\""
        return cmd_clean
    return cmd

def exec_cmd(host, cmd):
    cmd = c(host, cmd)
    print("command: ", cmd)
    os.system(cmd)

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
print(config)

for host, conf in config.items():
    print(f"Configuring: {host}\n")
    set_cc(host, conf["cc"])
    for command in conf["commands"]:
        exec_cmd(host, command)
