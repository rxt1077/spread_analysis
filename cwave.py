import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

start = 1.31
end = 1.34

x_array = []
y_array = []
z_array = []
with open('cwave.dat', 'r') as data_file:
    for line in data_file.readlines():
        split_line = line.split()
        x = int(split_line[0])/12000
        y = float(split_line[1])
        z = float(split_line[2])
        if x >= start:
            x_array.append(x)
            y_array.append(y)
            z_array.append(z)
        if x >= end:
            break

ax.plot(x_array, y_array, z_array)

plt.xlim([start, end])
plt.title('cwave')
ax.set_xlabel('time (s)')
ax.set_ylabel('real')
ax.set_zlabel('imag')
plt.savefig('cwave.png')
plt.close(fig)
