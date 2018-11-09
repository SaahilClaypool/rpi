import csv
import sys
import re
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt


def main():
    if (len(sys.argv) < 3):
        print("enter more args")
        exit(1)
    dirname = sys.argv[1]
    r_pattern = re.compile(".*{}.*.csv".format(sys.argv[2]))
    files = []
    for f in listdir(dirname):
        if (isfile(f) and r_pattern.match(str(f))):
            plot_one(f)
    
    plt.show()

def plot_one(filename):
    x = []
    y = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            x.append(float(row[0]) / 1000)
            y.append(float(row[1].strip()))

    plt.plot(x,y)

if __name__ == '__main__':
    main()
