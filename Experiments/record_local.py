#!/usr/bin/python3

import time
import os
import re
import sys
import time

# pattern = re.compile(b"backlog.*b")
pattern = (r"backlog (?P<num>\d*)b")
patternK = (r"backlog (?P<num>\d*)Kb")
patternM = (r"backlog (?P<num>\d*)Mb")

def main():
    t = 60
    out = sys.stdout
    if (len(sys.argv) > 1):
        t = int(sys.argv[1]) # seconds
    if (len(sys.argv) > 2):
        print("writing to: ", sys.argv[2])
        out = open(sys.argv[2], 'w')
    if (len(sys.argv) > 3):
        print("waiting for : ", sys.argv[3])
        time.sleep(int(sys.argv[3]))
    for i in range(int(t / .1)):
        buffer_len = get_current_buffer()
        print(time.time(), ",", buffer_len, file=out)
        time.sleep(.1)
    if (len(sys.argv) > 2):
        print("Finished writing to ", sys.argv[2], "after time", t)
        out.close()

def get_current_buffer():
    """
    return the current number of bytes in the tbf
    ignore the duplicate tbf and the netem queue
    output is always in bytes
    """

    # get the ouptut from the system call
    output = os.popen("sudo tc -s qdisc ls dev enp3s0").read()
    has_skipped_netem = False
    for line in output.split("\n"):
        # it looks like the tbf share a buffer
        # So, the we only need to recor the first one seen
        # break after the second one
        match = re.search(pattern, line)
        matchK = re.search(patternK, line)
        matchM = re.search(patternM, line)
        if (match):
            if (not has_skipped_netem):
                has_skipped_netem = True
                continue
            bytes_in_buffer = int(match.group("num"))
            return bytes_in_buffer
        elif (matchK):
            if (not has_skipped_netem):
                has_skipped_netem = True
                continue
            bytes_in_buffer = 100 * int(matchK.group("num"))
            return  bytes_in_buffer
        elif (matchM):
            if (not has_skipped_netem):
                has_skipped_netem = True
                continue
            bytes_in_buffer = 1000000 * int(matchM.group("num"))
            return bytes_in_buffer


if __name__ == "__main__":
    main()
