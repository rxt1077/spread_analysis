import matplotlib.pyplot as plt
import csv

fig = plt.figure()

x_list = []
y_list = []
start = 203500
end = 203700 
with open('fft.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x = int(row[0])
        if x >= start:
            x_list.append(x)
            y_list.append(float(row[1])**2+float(row[2])**2)
        if x >= end:
            break

plt.plot(x_list, y_list)
plt.savefig('fft.png')
plt.close(fig)
