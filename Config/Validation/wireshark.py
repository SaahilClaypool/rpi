#! /usr/bin/python3
import sys
import os
import re
import threading

if (len(sys.argv) < 2):
    print(f"enter the name of the experiment to open")
    exit()

name = sys.argv[1]
reg = re.compile(f"{name}.*")
for f in os.listdir("Results"):
    if (reg.match(f)):
        print(f"opening {f}")
        cmd = f"wireshark ./Results/{f}"
        t = threading.Thread(target=lambda : os.system(cmd))
        t.start()

