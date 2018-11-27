import matplotlib.pyplot as plt

tz = 0

x = []
y = []

with open("./output.csv") as csvfile:
    for line in csvfile:
        t, v = line.split(",")
        t = int(float(t))
        v = v.strip()
        v = int(v)
        if (tz == 0):
            tz = t

        x.append(t)
        y.append(v)
plt.plot(x,y)
plt.show()
