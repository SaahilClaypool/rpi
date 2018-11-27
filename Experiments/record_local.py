import time
import os
import re

# pattern = re.compile(b"backlog.*b")
pattern = (r"backlog (?P<num>\d*)b")
patternK = (r"backlog (?P<num>\d*)Kb")
patternM = (r"backlog (?P<num>\d*)Mb")

for i in range(int(60 / .1)):
    
    output = os.popen("sudo tc -s qdisc ls dev enp3s0").read()
    buffer_len = 0
    has_skipped_netem = False
    for line in output.split("\n"):
        match = re.search(pattern, line)
        matchK = re.search(patternK, line)
        matchM = re.search(patternM, line)
        if (match):
            if (not has_skipped_netem):
                has_skipped_netem = True
                continue
            bytes_in_buffer = int(match.group("num"))
            buffer_len += bytes_in_buffer
        elif (matchK):
            if (not has_skipped_netem):
                has_skipped_netem = True
                continue
            bytes_in_buffer = 100 * int(matchK.group("num"))
            buffer_len += bytes_in_buffer
        elif (matchM):
            if (not has_skipped_netem):
                has_skipped_netem = True
                continue
            bytes_in_buffer = 1000000 * int(matchM.group("num"))
            buffer_len += bytes_in_buffer


    # print(time.time(), ",", buffer_len)
    print(output)
    time.sleep(.1)
