import os
import time

with open("ss.txt", 'w') as outfile:
    while True:
        output = os.popen("ss -tin").read()
        print(output, file=outfile)
